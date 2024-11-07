# Graph-LoRA
A PyTorch Implementation of paper "Parameter-Efficient Fine-Tuning with Attributed Patch Semantic Graph for Automated Patch Correctness Assessment". 
## Introduction
Automatic program repair (APR) aims to automatically repair program errors without human intervention, and recent years have witnessed a growing research interest on this research topic. While much progress has been made and techniques originating from different disciplines have been proposed, APR techniques generally suffer from the patch overfitting issue, i.e., the generated patches are not genuinely correct despite they pass the employed tests. To alleviate this issue which overshadows the APR area, many research efforts have been devoted for automated patch correctness assessment (APCA). In particular, with the emergence of large language model (LLM) technology, many researchers have employed LLM to extract patch features and further assess the patch correctness. However, existing LLM-based methods typically treat code as token sequences and ignore the inherent formal structure for code, making it difficult to capture the deep patch semantics. To overcome the drawbacks, we in this paper design a novel patch graph representation named attributed patch semantic graph (APSG), which adequately captures the patch semantic and certain important, explicit patch attributes.![the structure of APSG.](APSG.png) For effectively using graph information in APSG, we accordingly propose a new parameter-efficient fine-tuning method of large language models named Graph-LoRA.
![the structure of Graph-LoRA.](Graph-LoRA.png)
## Folder Structure
Our code is written based on the Peft package. Here we only describe the files related to the implementation of our model. If you want to know about other files, please refer to Peft's project[https://github.com/huggingface/peft]
```
 ├── Dataset: data used to train and test
 ├── APSG: the code of APSG
     ├──APSG/semanticmodel: the code of generating semantic graphs
     ├──parser: the code of generating node attentions
 ├── peft: the code of peft
     ├──peft/tuners/lora/layer.py: the code of Graph-LoRA
     ├──peft/tuners/lora/attention.py: the code of attention
     ├──peft/tuners/lora/graph.py: the code of getting APSG features
 ├── train.py: code of training
 ├── test.py: code of testing
```
## Requirements
* Conda
  * install conda: [https://conda.io/projects/conda/en/latest/user-guide/install/index.html](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
  * Create a new conda environment:
      * if you are running with GPU: 
        ```
        conda env create -f environment-gpu.yml
        conda activate graphlora
        ```
        Dependencies include support for CUDA_11.4. If you are using a different CUDA version update the dependencies accordingly.
      * if you are running with CPU:   
        ```
        conda env create -f environment-cpu.yml
        conda activate graphlora
* Dataset
      * Wang data can be obtained from：[https://zenodo.org/record/3730599/files/Patches_for_Static.zip]
      * Lin data can be obtained from：[https://github.com/Ringbo/Cache/tree/master/patches/Small]
      * Balance data can be obtained from：[https://github.com/claudeyj/patch_correctness/tree/master/balanced_dataset]
## Dependency
* Python >= 3.8
* Pytorch >= 1.5.0
* Transformers>=4.10.0
* Deepspeed
* Numpy
* Scikit-learn
## Main code introduction
In order to allow readers to read the code of our model more accurately, we briefly introduce the main codes corresponding to the model structure.

The Graph-LoRA model mainly consists of three modules: (1)Attention, (2)Graph, (3)Graph-LoRA.
* (1) NARRepair model: the code to implement the NARRepair model is the NARRepair class in the NARRepair/narrepair/models/narrepair.py file
* (2) Code Encoder: this module will use the encoder part of the transformers model that comes with fairseq. Implemented in the NATransformerEncoder class in the fairseq/models/nat/narrepair_nonautoregressive_transformer file.
* (3) Repair Action Predictor: Implemented in the DurationPredictor class in the fairseq/models/nat/narrepair_nonautoregressive_transformer file.
* (4) Inter-word Dependency Extractor:Implemented in the Biaffine class and ast_link function in the fairseq/models/nat/narrepair_nonautodegrasive_transformer file.
* (5) Two-stage Decoder：Implemented in the NATransformerDecoder class in the fairseq/models/nat/narrepair_nonautoregressive_transformer file.
## Preprocess
Preprocessing is divided into two steps: (1) Obtain the repair actions of the training data (2) Convert the data into binary files.
### Obtain the repair actions
We divide all repair actions into: "insert", "delete", "replace", "keep". And we use dynamic programming method to obtain repair actions.
```
