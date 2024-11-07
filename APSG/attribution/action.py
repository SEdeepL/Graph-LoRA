import os
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
            add = False
            delete = False
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
                    delete=True
                elif line[0] == "+":
                    add = True
            if delete & add:
                print("replace")
            elif delete:
                print("delete")
            elif add:
                print(add)