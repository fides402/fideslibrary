import os
import json
import asyncio
from datetime import datetime
from zlibrary import AsyncZlib

ZLIB_EMAIL = os.environ['ZLIB_EMAIL']
ZLIB_PASSWORD = os.environ['ZLIB_PASSWORD']
today = datetime.today().strftime("%Y-%m-%d")

CATEGORIES = {
    "business": "Business Economics",
    "psychology": "Psychology",
    "selfhelp": "Self-Help Lifestyle",
    "society": "Society Politics Philosophy"
}

async def fetch_books():
    zlib = AsyncZlib()
    print("🔐 Connessione a Z-Library...")
    await zlib.login(ZLIB_EMAIL, ZLIB_PASSWORD)
    print("✅ Login effettuato con successo.")

    for category, query in CATEGORIES.items():
        print(f"🔎 Ricerca libri per '{category}'...")
        paginator = await zlib.search(q=query, count=12)  # 🔥 Rimosso year_from
        results = await paginator.next()

        books = []

        for item in results:
            book = await item.fetch()
            books.append({
                "title": item.get("name", "Senza titolo"),
                "author": item.get("authors", "Sconosciuto"),
                "link": item.get("mirror_1", item.get("url", "")),
                "cover": item.get("cover", ""),
                "category": category,
                "date": today
            })

        with open(f"data/{category}.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        print(f"📁 Salvati {len(books)} libri in 'data/{category}.json'.")

    await zlib.logout()
    print("🚪 Logout completato.")

if __name__ == "__main__":
    asyncio.run(fetch_books())
