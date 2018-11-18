import os

def write(filename,data):
    openMode = 'a'
    if os.path.exists(filename) == False:
        openMode = 'w'
    with open(filename,openMode) as f:
        for item in data:
            f.write(item)

# filename = 'write_data.txt'
# print(os.path.exists(filename)) # True

# with open(filename,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
#     f.write("I am Meringue.\n")
#     f.write("I am now studying in NJTECH.\n")

# with open(filename,'a') as f: # 'a'表示append,即在原来文件内容后继续写数据（不清除原有数据）
#     f.write("I major in Machine learning and Computer vision.\n")

# with open(filename) as f: 
#     # readline()每一次读取一行数据，并指向该行末尾
#     line1 = f.readline() # 读取第一行数据（此时已经指向第一行末尾）
#     line2 = f.readline() # 从上一次读取末尾开始读取（第二行）
#     print(line1.rstrip())
#     print(line2.rstrip())
