from pathlib import Path
import re

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "penal.txt": "clean_penal_code.txt",
    "civil.txt": "clean_civil_code.txt",
    "criminal_offence.txt": "clean_criminal_offence.txt",
    "domestic_violence.txt": "clean_domestic_violence.txt",
}


def clean_text(text: str) -> str:
    # Remove carriage returns
    text = text.replace("\r", "")
    # Remove repeated website header/footer
    text = re.sub(
        r"www\.lawcommission\.gov\.np",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove standalone page numbers
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)

    # Replace multiple spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def process_file(input_path: Path, output_path: Path):

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    cleaned_text = clean_text(text)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    print(f"Cleaned: {output_path.name}")


def main():

    for input_name, output_name in FILES.items():

        input_path = RAW_DIR / input_name
        output_path = PROCESSED_DIR / output_name

        if input_path.exists():
            process_file(input_path, output_path)
        else:
            print(f"Missing file: {input_name}")


if __name__ == "__main__":
    main()