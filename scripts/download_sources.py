from pathlib import Path
import re

import httpx
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
print("Root", ROOT)
OUTPUT = ROOT / "data" / "singapore"

SOURCES = [
    {
        "filename": "wikivoyage_singapore.md",
        "title": "Singapore — Travel guide at Wikivoyage",
        "source": "Wikivoyage",
        "url": "https://en.wikivoyage.org/wiki/Singapore",
    },
    {
        "filename": "visit_singapore_essential.md",
        "title": "Essential Singapore Travel Information",
        "source": "Visit Singapore",
        "url": "https://www.visitsingapore.com/travel-tips/essential-travel-information/",
    },
    {
        "filename": "visit_singapore_7_days.md",
        "title": "Enjoy Singapore in 7 Days",
        "source": "Visit Singapore",
        "url": "https://www.visitsingapore.com/content/visitsingapore/en/travel-tips/travelling-to-singapore/itineraries/7-days-in-singapore",
    },
    {
        "filename": "visit_singapore_itineraries.md",
        "title" : "Singapore Itineraries",
        "source" : "Visit Singapore",
        "url":"https://www.visitsingapore.com/singapore-itineraries/1-day-guide-to-jewel-changi/"
    }
]


def clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    text = soup.get_text("\n")
    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)

    return "\n".join(lines)


def download_source(item: dict) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with httpx.Client(
        timeout=30,
        follow_redirects=True,
        headers={"User-Agent": "AI-Travel-Planning-Assistant/1.0"},
    ) as client:
        response = client.get(item["url"])
        response.raise_for_status()

    body = clean_text(response.text)
    print("body", body)
    markdown = f"""---
title: "{item['title']}"
source: "{item['source']}"
url: "{item['url']}"
destination: "Singapore"
---

# {item['title']}

{body}
"""

    (OUTPUT / item["filename"]).write_text(
        markdown,
        encoding="utf-8",
    )

    print(f"Saved {item['filename']}")


if __name__ == "__main__":
    for item in SOURCES:
        download_source(item)

    print("Source download completed.")
    print("Review source reuse terms before redistributing downloaded content.")
