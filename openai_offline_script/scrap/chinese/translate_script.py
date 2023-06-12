# import os
# import numpy as np
# import openai
from googletrans import Translator
from dotenv import load_dotenv
# Load the .env file
load_dotenv()


lines = []
with open("meaning_sentences.txt", encoding="utf-8") as f:
    dream_meaning = f.read()
    dream_meaning = dream_meaning.split("\n")

print(len(dream_meaning))
for line in dream_meaning:
    if "|" not in line:
        continue
    if "股市" in line :
        continue
    line = line.split("|")[1]
    line = line.replace("\u3000", "")
    line = line.replace("\u3000", "")
    if not line.startswith("梦见") and not line.startswith("梦到"):
        continue
    lines.append(line)
lines = set(lines)
print(len(lines))
lines = list(lines)
#write to file name meaning_sentences_unique.txt
with open("meaning_sentences_unique.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line+"\n")

trans_result = []
with open("meaning_sentences_unique.txt", encoding="utf-8") as f:
    dream_meaning = f.read()
    dream_meaning = dream_meaning.split("\n")

def translate_text(text):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation.text

def translate_file(input_file, output_file, chunk_size=4000):
    with open(input_file, 'r', encoding='utf-8') as f_input:
        content = f_input.read()

    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    print(len(chunks))

    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translate_text(chunk)
        translated_chunks.append(translated_chunk)
        print(len(translated_chunks))

    translated_content = ''.join(translated_chunks)

    with open(output_file, 'w', encoding='utf-8') as f_output:
        f_output.write(translated_content)
# Example usage
input_file = 'meaning_sentences_unique.txt'
output_file = 'meaning_sentences_unique_trans.txt'
translate_file(input_file, output_file)

