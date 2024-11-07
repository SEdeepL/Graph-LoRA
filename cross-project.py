import os
import ipdb
# 指定你的目录路径
# ipdb.set_trace()
directory_path = '/mnt/yangzhenyu/llama-main/data/overfitting/Large/overfitting'

# 获取文件夹中的所有条目
entries = os.listdir(directory_path)

# 过滤出子目录
subdirectories = [d for d in entries if os.path.isdir(os.path.join(directory_path, d))]
for i in subdirectories:
    if i == "Many":
        continue
    directory1=directory_path+"/"+i
    entries1 = os.listdir(directory1)
    for j in entries1:
        directory2 =  directory1+"/"+j
        entries2 = os.listdir(directory2)
        for k in entries2:

            directory3 =  directory2+"/"+k
            print(directory3)
            with open(directory3, 'r') as file:
                lines = file.readlines()
            bug=[]
            patch=[]
            bugtext = []
            patchtext = []
            for line in lines:
                line = line.strip()
                if line[:3]=="---" or line[:3]=="+++" or line == "" or line[:4]=="diff" or line[0]=="/":
                    continue
                elif line[:2] == "@@":
                    print("start----------------")
                    if len(bugtext)!=0 and len(patchtext)!=0:
                        # ipdb.set_trace()
                        bug.append(bugtext.copy())
                        patch.append(patchtext.copy())
                        bugtext.clear()
                        patchtext.clear()
                elif line[0] == "-":
                    print("bug"+line[1:].strip())
                    bugtext.append(line[1:].strip())
                elif line[0] == "+":
                    print("fixed"+line[1:].strip())
                    patchtext.append(line[1:].strip())
                else:
                    print(line)
                    bugtext.append(line)
                    patchtext.append(line)
            # ipdb.set_trace()
            bug.append(bugtext.copy())
            patch.append(patchtext.copy())
            file_path = '/mnt/yangzhenyu/llama-main/data/overfitting/Large/overfittings.txt'
            # 打开文件，'a'表示追加模式
            with open(file_path, 'a') as file:
                for a in range(len(patch)):
                    file.write(" ".join(patch[a])+'\n')
