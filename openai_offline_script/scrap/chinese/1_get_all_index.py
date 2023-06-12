from bs4 import BeautifulSoup as bs
import requests
import re
import os
import json
import time
import random

def get_all_section():
    section_json = {}
    if os.path.exists('section.json'):
        with open('section.json', 'r') as f:
            section_json = json.load(f)
    else:
        url = "https://www.zgjm.org/a/"
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        tds = soup.find_all('td')
        section_text = []
        section_title = []
        for td in tds:
            as_ = td.find_all('a')
            #get text from a
            texts = [a.text for a in as_]
            hrefs = [a['href'] for a in as_]
            if len(texts) == 0:
                continue
            else:
                section_title.append(texts[-1])
                section_text.append(hrefs[-1])

        section_title, section_text = get_all_section()
        for i in range(len(section_title)):
            section_json[section_title[i]] = section_text[i]
        with open('section.json', 'w') as f:
            json.dump(section_json, f)

    return section_json

def get_items_in_section(section_json):
    item_json = {}
    if os.path.exists('items_links.json'):
        with open('items_links.json', 'r') as f:
            item_json = json.load(f)
    else: 
        for link in [x for x in  section_json.values()][2:]:
            response = requests.get(link)
            soup = bs(response.text, 'html.parser')
            div = soup.find('div', id='list')
            lis = div.find_all('li')
            hrefs = [li.find('a')['href'] for li in lis]
            texts = [li.find('a').text for li in lis]
            for i in range(len(texts)):
                item_json[texts[i]] = hrefs[i]
        with open('items_links.json', 'w') as f:
            json.dump(item_json, f)
    return item_json


def get_all_meanings(item_json):
    for item in item_json:
        if os.path.exists(f'dream_meaning\\meanings_{item}.txt'):
            continue
        time.sleep(random.randint(1,2))
        url="https://www.zgjm.org"+item_json[item]
        print(url)
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        div = soup.find('div', class_='read-content')
        ps = div.find_all('p')
        meaning = [p.text for p in ps]
        #write to file
        with open(f'dream_meaning\\meanings_{item}.txt', 'w', encoding="utf-8") as f:
            f.write('\n'.join(meaning))

                    


section_json = get_all_section()
item_json = get_items_in_section(section_json)
get_all_meanings(item_json)

print(len(section_json))
print(len(item_json))