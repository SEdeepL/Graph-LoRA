import torch
from peft import LoraConfig, get_peft_model 
from transformers import TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer
from datasets import Dataset
import ipdb
train_dataset=[]
val_dataset=[]

tf = open("/mnt/HDD/yangzhenyu/llama-main/data/train.txt") # 返回一个文件对象
line = tf.readline()
while line:
    en,ch,_=line.split("	")
    train_dataset.append({'text': 'Translate English to chinese:\nInput:'+ en + '\nOutput:'+ ch + '</s>'})
    line = tf.readline()
tf.close()
ef = open("/mnt/HDD/yangzhenyu/llama-main/data/eval.txt") # 返回一个文件对象
line = ef.readline()
while line:
    en,ch,_=line.split("	")
    val_dataset.append({'text': 'Translate English to chinese:\nInput:'+ en + '\nOutput:'+ ch + '</s>'})
    line = ef.readline()
ef.close()
train_dataset = Dataset.from_dict({key: [dic[key] for dic in train_dataset] for key in train_dataset[0]})
val_dataset = Dataset.from_dict({key: [dic[key] for dic in val_dataset] for key in val_dataset[0]})
# ipdb.set_trace()
peft_config = LoraConfig(
    r=8,
    target_modules=['q_proj','v_proj'],
    lora_dropout = 0.05,
    bias='none',
    task_type='CAUSAL_LM'
)
# 配置训练参数
training_aruments = TrainingArguments(
    output_dir="/mnt/HDD/yangzhenyu/llama-main/check_point",# 模型输出的目录
    per_device_train_batch_size=64,
    optim='adamw_torch',
    learning_rate=10e-4,
    eval_steps=50,
    save_steps=100,
    logging_steps=20,
    evaluation_strategy='steps',
    group_by_length=False,
    # num_train_epochs=2，#训练的epoch数，和下面的max_steps二选一
    max_steps=200,
    gradient_accumulation_steps=1,
    gradient_checkpointing=True,
    max_grad_norm=0.3,
    bf16=True,
    lr_scheduler_type='cosine',
    warmup_steps=100
)
model_name ='/mnt/HDD/yangzhenyu/llama2-hf/'
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map='auto'
)
ipdb.set_trace()

# model.gradient_checkpointing_enable()# 和下面的enable_input_require_grads()均可
model.enable_input_require_grads()
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
model.config.use_cache = False
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token_id = 0
tokenizer.padding_side = 'right'
# ipdb.set_trace()
trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    dataset_text_field='text',
    peft_config=peft_config,
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_aruments
)
trainer.train()
trainer.model.save_pretrained("/mnt/HDD/yangzhenyu/llama-main/trainedmodel")