import os
import json
import asyncio
from datetime import datetime
from zlibrary import AsyncZlib, Language

# Prendi le credenziali da variabili d'ambiente (GitHub Secrets)
ZLIB_EMAIL = os.environ['ZLIB_EMAIL']
ZLIB_PASSWORD = os.environ['ZLIB_PASSWORD']
today = datetime.today().strftime("%Y-%m-%d")

# Query per ciascuna categoria
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
        print(f"🔍 Ricerca per categoria: {category}")

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

            # Estrazione e pulizia degli autori
            authors_raw = book.get("authors", [])
            if isinstance(authors_raw, list):
                authors = ", ".join(
                    a.get("name", "Sconosciuto") if isinstance(a, dict) else str(a)
                    for a in authors_raw
                )
            else:
                authors = authors_raw or "Sconosciuto"

            books.append({
                "title": book.get("name", "Senza titolo"),
                "author": authors,
                "link": book.get("mirror_1", book.get("url", "")),
                "cover": book.get("cover", ""),
                "category": category,
                "language": book.get("language", ""),
                "year": book.get("year", ""),
                "date": today
            })

        # Salva nel file JSON
        file_path = f"data/{category}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        print(f"📁 Salvati {len(books)} libri in '{file_path}'.")

    await zlib.logout()
    print("🚪 Logout completato.")

if __name__ == "__main__":
    asyncio.run(fetch_books())
