import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")

# Dizionario di categorie e URL corrispondenti
CATEGORIES = {
    "business": "https://1lib.sk/category/5/Business--Economics/s/?yearFrom=2025&languages[]=italian&languages[]=english&order=date",
    "psychology": "http://1lib.sk/category/29/Psychology/s/?yearFrom=2025&linguals[]=italian&linguals[]=english&order=date",
    "selfhelp": "https://1lib.sk/category/35/Self-Help-Relationships--Lifestyle/s/?yearFrom=2025&linguals[]=italiano&linguals[]=english&order=date",
    "society": "https://1lib.sk/category/36/Society-Politics--Philosophy/s/?yearFrom=2025&linguals[]=italiano&linguals[]=english&order=date"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def estrai_libri(url, category):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    books = []

    for item in soup.select(".resItemBox")[:12]:  # Limitiamo ai primi 12 libri
        try:
            title = item.select_one(".bookTitle").get_text(strip=True)
            author = item.select_one(".authors").get_text(strip=True)
            link = "https://1lib.sk" + item.select_one("a")["href"]
            img = item.select_one("img")["src"]
            if img.startswith("//"):
                img = "https:" + img

            books.append({
                "title": title,
                "author": author,
                "link": link,
                "cover": img,
                "category": category,
                "date": today
            })
        except Exception as e:
            print(f"Errore parsing libro: {e}")
    return books

# Scrive i dati per ciascuna categoria
for category, url in CATEGORIES.items():
    print(f"Aggiorno {category}...")
    libri = estrai_libri(url, category)
    with open(f"data/{category}.json", "w", encoding="utf-8") as f:
        json.dump(libri, f, ensure_ascii=False, indent=2)
    print(f"Salvati {len(libri)} libri in data/{category}.json")
