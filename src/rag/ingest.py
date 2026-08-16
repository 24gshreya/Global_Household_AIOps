from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
}


def load_knowledge_documents(
    knowledge_dir: str | Path,
) -> list[dict]:

    knowledge_path = Path(knowledge_dir)

    documents = []

    for file_path in knowledge_path.rglob("*"):

        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        ):

            text = file_path.read_text(
                encoding="utf-8"
            )

            documents.append(
                {
                    "source": str(file_path),
                    "text": text,
                }
            )

    return documents