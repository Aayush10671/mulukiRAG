from pathlib import Path
import pymupdf 

DATA_DIR = Path("data/external")
RAW_DIR = Path("data/raw")

RAW_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path: Path, output_path: Path):

    document = pymupdf.open(pdf_path)

    all_text = ""

    for page in document:
        text = page.get_text()
        all_text += text + "\n"

    document.close()

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(all_text)

    print(f"Saved: {output_path}")


def main():
    files = {
        "penal_code.pdf": "penal.txt",
        "civil_code.pdf": "civil.txt",
        "criminal_offence.pdf":"criminal_offence.txt",
        "domestic_violence.pdf":"domestic_violence.txt"
    }

    for pdf_name, txt_name in files.items():
        pdf_path = DATA_DIR / pdf_name
        output_path = RAW_DIR / txt_name

        if pdf_path.exists():
            extract_text_from_pdf(pdf_path, output_path)
        else:
            print(f"Missing: {pdf_path}")


if __name__ == "__main__":
    main()