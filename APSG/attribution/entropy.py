import os, sys, json, math
from alpha_repair_code.model import *
from os.path import *
import torch
def extract_common_prefix_tokens(tokens_1:torch, tokens_2:torch):
    tokens_1 = tokens_1.to(lm.model.device)
    tokens_2 = tokens_2.to(lm.model.device)
    for i in range(min(len(tokens_1), len(tokens_2))):
        if tokens_1[i] != tokens_2[i]:
            return tokens_1[:i]
        
def extract_common_prefix_str(output_str, target_str):
    # target_str should have been stripped
    print('DEBUG: output_str: ', output_str)
    print('DEBUG: target_str: ', target_str)
    striped_output_str = output_str.lstrip() # remove leading spaces, tabs, newlines
    striped_str = output_str[:len(output_str) - len(striped_output_str)]
    for i in range(min(len(striped_output_str), len(target_str))):
        if striped_output_str[i] != target_str[i]:
            return output_str[:len(striped_str) + i], striped_str
    return output_str[:len(striped_str) + min(len(striped_output_str), len(target_str))], striped_str

def str_2_tokens(str:str):
    return lm.tokenizer.encode(str, return_tensors='pt', add_special_tokens=False)[0]

def tokens_2_str(tokens:torch):
    return lm.tokenizer.decode(tokens, skip_special_tokens=True)

def load_vocab(vocab_path):
    with open(vocab_path, 'r') as f:
        vocab = json.load(f)
    return vocab

def concat_encoded_tokens(token_tensor_1, token_tensor_2):
    # shape of token_tensor_1 and token_tensor_2: (1, seq_len)
    token_tensor_1 = token_tensor_1.to(lm.model.device)
    token_tensor_2 = token_tensor_2.to(lm.model.device)
    return torch.cat((token_tensor_1[0][:], token_tensor_2[0][:])).unsqueeze(0)

def concat_encoded_tokens_list(token_tensor_list):
    # shape of element in token_tensor_list: (1, seq_len)
    if len(token_tensor_list) == 1:
        return token_tensor_list[0]
    else:
        return concat_encoded_tokens(token_tensor_list[0], concat_encoded_tokens_list(token_tensor_list[1:]))

def build_input(prefix: str, suffix: str) -> str:
    return prefix + infill_ph + suffix
    
def get_scores(prefix_tokens:torch, suffix_tokens:torch, target_tokens:torch, scores:list):
    # prefix and suffix are stripped encoded tokens
    # target_tokens should also be stripped encoded tokens
    if len(target_tokens) == 0:
        return
    lst = []
    # torch.tensor[[1]], prefix_tokens, torch.tensor[[32099]], suffix_tokens, torch.tensor[[2]]
    lst.append(torch.tensor([[1]]))
    lst.append(prefix_tokens)
    lst.append(torch.tensor([[32099]]))
    lst.append(suffix_tokens)
    lst.append(torch.tensor([[2]]))
    input_tokens = concat_encoded_tokens_list(lst) # shape: (1, seq_len)
    target_tokens = target_tokens.to(lm.model.device)
    
    with torch.no_grad():
        lm.model.reinit(lm.tokenizer, False, set(), 'java', '', '')
        raw_o = lm.model.generate(input_tokens,
                                     max_length=50,
                                     do_sample=True,
                                     output_scores=True,
                                     return_dict_in_generate=True,
                                     temperature=1,
                                     top_k=200,
                                     top_p=1,
                                     use_cache=True)
        t_outputs = lm.model.tokenizer.batch_decode(raw_o.sequences, skip_special_tokens=False)
        t_output = t_outputs[0]
        assert infill_ph in t_output, 'infill_ph not in output' + raw_o.sequences[0]
        next_target_token = target_tokens[0]
        min_index = raw_o.sequences[0, 1:].tolist().index(token_2_id_vocab[infill_ph])
        next_target_token_score_dist = raw_o.scores[min_index + 1][0].softmax(dim=0) # 0 here means the first batch
        score_next_target_token = next_target_token_score_dist[next_target_token] 
    
    scores.append(score_next_target_token.item())
    get_scores(concat_encoded_tokens(prefix_tokens, torch.tensor([[next_target_token]])), suffix_tokens, target_tokens[1:], scores)
     
def get_entropy(prefix:str, suffix:str, patch:str):
    prefix_tokens = lm.tokenizer.encode(prefix, return_tensors='pt', add_special_tokens=False)[0].unsqueeze(0)
    suffix_tokens = lm.tokenizer.encode(suffix, return_tensors='pt', add_special_tokens=False)[0].unsqueeze(0)
    target_tokens = lm.tokenizer.encode(patch, return_tensors='pt', add_special_tokens=False)[0]
    
    torch.cuda.empty_cache()
    scores = []
    get_scores(prefix_tokens, suffix_tokens, target_tokens, scores)
    scores = [score if score > 0 else MIN_SCORE for score in scores]
    print('DEBUG: scores: ', scores)
    
    neg_logs = [-math.log(score) for score in scores]
    sum_entropy = sum(neg_logs)
    return sum_entropy