import os
import json

content = {}
# read files C:\@code\chatdream_app\meaning_sentences.txt
with open('meaning_sentences.txt', 'r', encoding="utf-8") as f:
    meaning_sentences = f.read()
    
    meaning_sentences = meaning_sentences.split('\n')
    meaning_sentences = [x for x in meaning_sentences if x != '']
    # remove duplicate lines
    meaning_sentences = list(set(meaning_sentences))
    for item in meaning_sentences:
        index = item.split('|')[0]
        meaning = item.split('|')[1]
        meaning = meaning.strip()

        if index not in content:
            content[index] = {}
        
        if 'meaning' in content[index]:
            if meaning not in content[index]['meaning']:
                content[index]['meaning'].append(meaning)
                content[index]['meaning_len'].append(len(meaning))
            else:
                print("duplicate meaning", index, meaning)
        else:
            content[index]['meaning'] = [meaning]
            content[index]['meaning_len'] = [len(meaning)]


# read files C:\@code\chatdream_app\old_book_sources.txt
with open('old_book_sources.txt', 'r', encoding="utf-8") as f:
    old_book_sources = f.read()
    old_book_sources = old_book_sources.split('\n')
    old_book_sources = [x for x in old_book_sources if x != '']
    # remove duplicate lines
    old_book_sources = list(set(old_book_sources))
    for item in old_book_sources:
        index = item.split('|')[0]
        meaning = item.split('|')[1]
        meaning = meaning.strip()

        if index not in content:
            print("index not found", index)
        else:
            if 'old_book' in content[index]:
                if meaning not in content[index]['old_book']:
                    content[index]['old_book'].append(meaning)
                else:
                    print("duplicate old_book", index, meaning)
            else:
                content[index]['old_book'] = [meaning]


# read files C:\@code\chatdream_app\phycos.txt
with open('phycos.txt', 'r', encoding="utf-8") as f:
    phycos = f.read()
    phycos = phycos.split('\n')
    phycos = [x for x in phycos if x != '']
    # remove duplicate lines
    phycos = list(set(phycos))
    for item in phycos:
        index = item.split('|')[0]
        meaning = item.split('|')[1]
        meaning = meaning.strip()

        if index not in content:
            print("index not found", index)
        else:
            if 'phycos' in content[index]:
                if meaning not in content[index]['phycos']:
                    content[index]['phycos'].append(meaning)
                else:
                    print("duplicate phycos", index, meaning)
            else:
                content[index]['phycos'] = [meaning]
print("total", len(content))


# write content to json files
with open('content.json', 'w', encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=4)
