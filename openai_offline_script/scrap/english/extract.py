import requests
from bs4 import BeautifulSoup
import time

for char in 'abcdefghijklmnopqrstuvwxyz':
        
    url = f'https://www.dreamdictionary.org/{char}/'
    session = requests.Session()
    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    response = session.get(url)
    time.sleep(5)

    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='interpretation')
    print("items count: ",len(divs))
    p_tags = [div.find_all('p') for div in divs]

    save_path = f'dream_meaning\english\dreams_dict_en_{char}.txt'
    with open(save_path, 'w', encoding='utf-8') as f:
        for p in p_tags:
            line = p[0].text+"|"+p[1].text+"\n"
            f.write(line)
