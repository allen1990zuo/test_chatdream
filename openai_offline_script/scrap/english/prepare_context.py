import os
# read all text files in the folder

path = "C:\@code\chatdream_app\dream_meaning\english"

files = os.listdir(path)
files_txt = [path+"\\"+i for i in files if i.endswith('.txt')]
# merge all text files into one

with open('context/dream_dict_context.txt', 'w', encoding='utf-8') as f:
    pass
for path_txt in files_txt:
    with open(path_txt, 'r', encoding='utf-8') as f:
        text = f.read()
    with open('context/dream_dict_context.txt', 'a', encoding='utf-8') as f:
        f.write(text)
