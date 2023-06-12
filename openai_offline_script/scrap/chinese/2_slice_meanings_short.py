import pandas as pd
import os
import re
# read all meanings file txt in a loop
files = os.listdir('dream_meaning')

phycos = []
old_book_sources = []
meaning_sentences = []
indces = []
for file in files:
    index = file.split('_')[1].split('.')[0]
    index = index+"|"
    indces += index
    with open(f'dream_meaning\\{file}', 'r', encoding="utf-8") as f:
        meanings = f.read()
        meanings = meanings.replace("周公解梦官网", "")
        meanings = meanings.replace("(周公解梦)", "")
        meanings = meanings.replace("(周公解梦", "")
        meanings = meanings.replace("周易解梦", "")
        meanings = meanings.replace("来自 周公解梦", "")
        meanings = meanings.replace("(由原创首发)", "")
        meanings = meanings.replace("(来源", "")
        meanings = meanings.replace("(由", "")
        meanings = meanings.split('\n')
        meanings = meanings[1:]
        meanings = [x for x in meanings if x != '']
        meanings = [x for x in meanings if len(x) >2]

        for i in range(len(meanings)):

            meanings[i] = re.sub(r'http\S+', '', meanings[i])
            meanings[i] = re.sub(r'www\S+', '', meanings[i])
            meanings[i] = re.sub(r'wWw\S+', '', meanings[i])
            meanings[i] = re.sub(r'WWW\S+', '', meanings[i])
            meanings[i] = re.sub(r'Www\S+', '', meanings[i])
            meanings[i] = re.sub(r'wwW\S+', '', meanings[i])
            meanings[i] = re.sub(r'wWW\S+', '', meanings[i])
            meanings[i] = re.sub(r'ZGJM\S+', '', meanings[i])
            meanings[i] = re.sub(r'zgjm\S+', '', meanings[i])

        phyco = []
        for i in range(len(meanings)):
            if '梦境解说' in meanings[i]:
                phyco.append(index + meanings[i])
                meanings[i] = ''
            if '心理分析' in meanings[i]:
                phyco.append(index + meanings[i])
                meanings[i] = ''
            if '精神象征' in meanings[i]:
                phyco.append(index + meanings[i])
                meanings[i] = ''
        phycos += phyco

        old_book_source = []
        for i in range(len(meanings)):
            if'《' in meanings[i]:
                old_book_source.append(index + meanings[i])
                meanings[i] = ''
        old_book_sources += old_book_source

        truncate_list = ["心理学解梦", "原版周公解梦", "的案例分析", "周公股市"]

        meanings_filter=[]
        for x in meanings:
            if "心理学解梦" in x:
                break
            elif "原版周公解梦" in x:
                break
            elif "的案例分析" in x:
                break
            elif "meanings" in x:
                break
            else:
                meanings_filter.append(x)

        meanings = meanings_filter
        meanings = [x for x in meanings if x != '']
        meanings = [index + x for x in meanings]
        meaning_sentences += meanings

phycos = [x.strip() for x in phycos]
phycos = sorted(list(set(phycos)))
with open('phycos.txt', 'w', encoding="utf-8") as f:
    for item in phycos:
        f.write("%s\n" % item)

old_book_sources = [x.strip() for x in old_book_sources]
old_book_sources = sorted(list(set(old_book_sources)))
with open('old_book_sources.txt', 'w', encoding="utf-8") as f:
    for item in old_book_sources:
        f.write("%s\n" % item)

meaning_sentences = [x.strip() for x in meaning_sentences]
meaning_sentences = sorted(list(set(meaning_sentences)))
with open('meaning_sentences.txt', 'w', encoding="utf-8") as f:
    for item in meaning_sentences:
        f.write("%s\n" % item)


# check number of characters in meaning_sentences
number_of_characters = 0
for meaning_sentence in meaning_sentences:
    number_of_characters += len(meaning_sentence)
print("number_of_characters", number_of_characters)

# check number of characters in meaning_sentences
number_of_characters = 0
for x in indces:
    number_of_characters += len(x)
print("number_of_characters", number_of_characters)
print("price estimation  = ", 0.0004*number_of_characters)

# check number of characters in old_book_sources
number_of_characters = 0
for old_book_source in old_book_sources:
    number_of_characters += len(old_book_source)
print("number_of_characters", number_of_characters)
# check number of characters in phycos
number_of_characters = 0
for phyco in phycos:
    number_of_characters += len(phyco)
print("number_of_characters", number_of_characters)