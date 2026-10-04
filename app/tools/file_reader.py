from pathlib import Path


def read_text_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported for now.")

    return path.read_text(encoding="utf-8")
