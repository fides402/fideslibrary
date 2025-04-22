import json
import requests
from bs4 import BeautifulSoup

def estrai_libri(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    books = []
    for el in soup.select('.resItemBox'):
        title = el.select_one('.bookTitle').text.strip()
        author = el.select_one('.authors').text.strip()
        link = "https://1lib.sk" + el.select_one('a')['href']
        books.append({
            "title": title,
            "author": author,
            "link": link,
            "cover": "",  # opzionale
            "category": "business",  # da variare per sezione
            "date": "2025-04-23"
        })
    return books

with open("data/business.json", "w", encoding="utf-8") as f:
    json.dump(estrai_libri("https://1lib.sk/category/5/..."), f, indent=2, ensure_ascii=False)
# Ripeti per le altre categorie
