from pathlib import Path
import re

from langchain_core.documents import Document


DATA_DIRECTORY = Path("data/singapore")


def _parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}, text

    raw = parts[1]
    body = parts[2].lstrip()
    metadata = {}

    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body


def load_markdown_documents(data_directory: Path = DATA_DIRECTORY) -> list[Document]:
    documents: list[Document] = []

    for file_path in sorted(data_directory.glob("*.md")):
        if file_path.name.lower() in {"readme.md", "sources.md"}:
            continue

        text = file_path.read_text(encoding="utf-8")
        metadata, body = _parse_front_matter(text)

        metadata.setdefault("file_name", file_path.name)
        metadata.setdefault("destination", "Singapore")

        documents.append(
            Document(
                page_content=body.strip(),
                metadata=metadata,
            )
        )

    if not documents:
        raise FileNotFoundError(
            f"No knowledge-base markdown files found in {data_directory}. "
            "Run scripts/download_sources.py or add approved source documents."
        )

    return documents
