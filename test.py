import torch
from transformers import LlamaTokenizer, LlamaForCausalLM,AutoTokenizer
from peft import PeftModel

base_model_path = '/mnt/HDD/yangzhenyu/llama2-hf'
finetune_model_path ='/mnt/HDD/yangzhenyu/llama-main/check_point'
nerged_model_path='/mnt/HDD/yangzhenyu/llama-main/llama-2-7b-merged'
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
#先加载基座模型，再加入finetune后的参
model = LlamaForCausalLM.from_pretrained(base_model_path, load_in_8bit=False, device_map='auto', torch_dtype=torch.float16)
model = PeftModel.from_pretrained(model, finetune_model_path)
test_prompt = """
Translate English to Chinese:
Input:I want a book.
0utput:
"""
model_input = tokenizer(test_prompt, return_tensors='pt')
model.eval()
with torch.no_grad():
    res = model.generate(**model_input, max_new_tokens=100)[0]
    print(tokenizer.decode(res,skip_special_tokens=True))