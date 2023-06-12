import pandas as pd
import os
# read all meanings file txt in a loop
files = os.listdir('dream_meaning')

phycos=[]
old_book_sources=[]
meaning_sentences=[]

for file in files:
    index=file.split('_')[1].split('.')[0]
    with open(f'dream_meaning\\{file}', 'r', encoding="utf-8") as f:
        meanings = f.read()
        meanings = meanings.split('\n')
        meanings = [meaning for meaning in meanings if meaning != '']
        meanings = meanings[1:]
        
        phyco=[]
        for i in range(len(meanings)):
            if '梦境解说' in meanings[i]:
                phyco.append(index + meanings[i])
            if '心理分析' in meanings[i]:
                phyco.append(index + meanings[i])
            if '精神象征' in meanings[i]:
                phyco.append(index + meanings[i])
        phycos+=phyco
            
        old_book_source = []
        for i in range(len(meanings)):
            if'《'in meanings[i]:
                old_book_source.append(meanings[i])
        old_book_sources+=old_book_source

        meaning_sentence = meanings
        for i in range(len(meanings)):
            if '周公股市' in meanings[i] or '案例分析' in meanings[i] or '心理学解梦' in meanings[i] or '原版周公解梦' in meanings[i]:
                meaning_sentence = meanings[:i]
                break
        meaning_sentence = [meaning for meaning in meaning_sentence if meaning != '']
        meaning_sentence = [meaning for meaning in meaning_sentence if meaning != '\t']

        meaning_sentences+=meaning_sentence

# write to txt
with open('phycos.txt', 'w', encoding="utf-8") as f:
    for item in phycos:
        f.write("%s\n" % item)
# strip space old_book_sources
old_book_sources = [old_book_source.strip() for old_book_source in old_book_sources]
old_book_sources = sorted(list(set(old_book_sources)))
with open('old_book_sources.txt', 'w', encoding="utf-8") as f:
    for item in old_book_sources:
        f.write("%s\n" % item)
#remove www.zGjm.org from meaning_sentences
meaning_sentences = [meaning_sentence.replace('www.zGjm.org','') for meaning_sentence in meaning_sentences]

meaning_sentences = [meaning_sentence.strip() for meaning_sentence in meaning_sentences]
meaning_sentences = sorted(list(set(meaning_sentences)))
with open('meaning_sentences.txt', 'w', encoding="utf-8") as f:
    for item in meaning_sentences:
        f.write("%s\n" % item)


# check number of characters in meaning_sentences
number_of_characters = 0
for meaning_sentence in meaning_sentences:
    number_of_characters+=len(meaning_sentence)
print("number_of_characters",number_of_characters)
#check number of characters in old_book_sources
# number_of_characters = 0
for old_book_source in old_book_sources:
    number_of_characters+=len(old_book_source)
print("number_of_characters",number_of_characters)
#check number of characters in phycos
# number_of_characters = 0
for phyco in phycos:
    number_of_characters+=len(phyco)
print("number_of_characters",number_of_characters)

print("price estimation  = ",0.0004*number_of_characters)