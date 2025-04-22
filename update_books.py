import os
import json
import asyncio
from datetime import datetime
from zlibrary import AsyncZlib, Language

# Credenziali prese dai GitHub Secrets
ZLIB_EMAIL = os.environ['ZLIB_EMAIL']
ZLIB_PASSWORD = os.environ['ZLIB_PASSWORD']
today = datetime.today().strftime("%Y-%m-%d")

# Query per categoria
CATEGORIES = {
    "business": "Business Economics",
    "psychology": "Psychology",
    "selfhelp": "Self-Help Lifestyle",
    "society": "Society Politics Philosophy"
}

async def fetch_books():
    zlib = AsyncZlib()
    await zlib.login(ZLIB_EMAIL, ZLIB_PASSWORD)
    print("✅ Login effettuato con successo.")

    for category, query in CATEGORIES.items():
        print(f"🔍 Ricerca per: {category}")
        paginator = await zlib.search(
            q=query,
            count=50,
            from_year=2025,
            to_year=2025,
            lang=[Language.ENGLISH, Language.ITALIAN]
        )
        results = await paginator.next()
        books = []

        for item in results:
            book = await item.fetch()

            authors_raw = book.get("authors", [])
            authors = ", ".join(authors_raw) if isinstance(authors_raw, list) else authors_raw

            books.append({
                "title": book.get("name", "Senza titolo"),
                "author": authors or "Sconosciuto",
                "link": book.get("mirror_1", book.get("url", "")),
                "cover": book.get("cover", ""),
                "category": category,
                "language": book.get("language", ""),
                "year": book.get("year", ""),
                "date": today
            })

        with open(f"data/{category}.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        print(f"📁 Salvati {len(books)} libri in data/{category}.json")

    await zlib.logout()
    print("🚪 Logout completato.")

if __name__ == "__main__":
    asyncio.run(fetch_books())
