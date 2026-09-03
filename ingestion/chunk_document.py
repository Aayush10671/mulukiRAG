from pathlib import Path
import json
import re

PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)


FILES = {
    "clean_penal_code.txt": "National-Penal-Code",
    "clean_civil_code.txt": "National-Civil-Code",
    "clean_criminal_offence.txt": "Criminal-Offences-Sentencing-and-Execution-Act",
    "clean_domestic_violence.txt": "Domestic-Violence-Act",
}

# Part-1
# Part -1
# Part – 1
# Part 1
PART_PATTERN = re.compile(
    r"^\s*Part\s*[-–—]?\s*(\d+)\s*$",
    re.IGNORECASE
)
# Chapter-1
# Chapter - 1
# Chapter – 2
# Chapter 3
CHAPTER_PATTERN = re.compile(
    r"^\s*Chapter\s*[-–—]?\s*(\d+)\s*$",
    re.IGNORECASE
)


# ------------------------------------------------------------
# SECTION
#
# This is the important change.
#
# It matches BOTH:
#
# 1.
# Short title...
#
# AND:
#
# 308. Statute of limitation:
#
# It does NOT match:
#
# (1)
# (2)
# (a)
# (b)
# ------------------------------------------------------------

SECTION_PATTERN = re.compile(
    r"^\s*(\d+)\.\s*(.*)$"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_line(line):
    """Normalize whitespace in a line."""

    line = line.replace("\r", "")
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def is_page_number(line):
    """
    Detect a line that contains only a number.

    Example:
        1
        25
        103

    These are PDF page numbers and should not become sections.
    """

    return bool(re.fullmatch(r"\d+", line.strip()))

def is_part(line):
    """Check whether a line is a Part heading."""

    return bool(PART_PATTERN.match(line))


def is_chapter(line):
    """Check whether a line is a Chapter heading."""

    return bool(CHAPTER_PATTERN.match(line))


def is_section(line):
    """
    Check whether a line starts with a top-level section number.

    Examples:

        1. Short title
        16. Limitation
        308. Statute of limitation
        1.

    Does not match:

        (1)
        (2)
        (a)
        (b)
    """

    return bool(SECTION_PATTERN.match(line))


# ============================================================
# CREATE CHUNK
# ============================================================

def create_chunk(
    source,
    part_number,
    part_title,
    chapter_number,
    chapter_title,
    section_number,
    section_title,
    section_lines
):
    """Create one section-level chunk."""

    source_id = re.sub(
        r"[^a-z0-9]+",
        "_",
        source.lower()
    ).strip("_")

    part_id = (
        f"part_{part_number}"
        if part_number is not None
        else "part_none"
    )

    chapter_id = (
        f"chapter_{chapter_number}"
        if chapter_number is not None
        else "chapter_none"
    )

    chunk_id = (
        f"{source_id}_"
        f"{part_id}_"
        f"{chapter_id}_"
        f"section_{section_number}"
    )

    text = "\n".join(section_lines).strip()

    return {
        "chunk_id": chunk_id,
        "source": source,

        "part_number": part_number,
        "part_title": part_title,

        "chapter_number": chapter_number,
        "chapter_title": chapter_title,

        "section_number": section_number,
        "section_title": section_title,

        "text": text
    }


# ============================================================
# PARSE DOCUMENT
# ============================================================

def parse_document(text, source):
    """
    Parse a legal document into section-level chunks.

    Structure:

        Part (optional)
            ↓
        Chapter (optional)
            ↓
        Section
            ↓
        Subsections / Clauses

    A section can appear as:

        1.
        Section title...

    OR:

        1. Section title...

    Subsections such as (1), (2), (a), (b) remain inside
    their parent section.
    """

    raw_lines = text.splitlines()

    lines = []

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    for raw_line in raw_lines:

        line = normalize_line(raw_line)

        if not line:
            continue

        # Remove PDF page numbers
        if is_page_number(line):
            continue

        # Remove website text if still present
        if "www.lawcommission.gov.np" in line.lower():
            continue

        lines.append(line)

    # ========================================================
    # CURRENT METADATA
    # ========================================================

    part_number = None
    part_title = None

    chapter_number = None
    chapter_title = None

    section_number = None
    section_title = None
    section_lines = []

    chunks = []

    i = 0

    # ========================================================
    # PROCESS EVERY LINE
    # ========================================================

    while i < len(lines):

        line = lines[i]

        # ====================================================
        # PART
        # ====================================================

        part_match = PART_PATTERN.match(line)

        if part_match:

            # Save previous section
            if section_number is not None:

                chunks.append(
                    create_chunk(
                        source,
                        part_number,
                        part_title,
                        chapter_number,
                        chapter_title,
                        section_number,
                        section_title,
                        section_lines
                    )
                )

            # Reset current section
            section_number = None
            section_title = None
            section_lines = []

            # Store part number
            part_number = part_match.group(1)

            # Part title is normally on the next line
            part_title = None

            if i + 1 < len(lines):

                next_line = lines[i + 1]

                if (
                    not is_part(next_line)
                    and not is_chapter(next_line)
                    and not is_section(next_line)
                ):
                    part_title = next_line
                    i += 1

            i += 1
            continue

        # ====================================================
        # CHAPTER
        # ====================================================

        chapter_match = CHAPTER_PATTERN.match(line)

        if chapter_match:

            # Save previous section
            if section_number is not None:

                chunks.append(
                    create_chunk(
                        source,
                        part_number,
                        part_title,
                        chapter_number,
                        chapter_title,
                        section_number,
                        section_title,
                        section_lines
                    )
                )

            # Reset current section
            section_number = None
            section_title = None
            section_lines = []

            # Store chapter number
            chapter_number = chapter_match.group(1)

            # Chapter title is normally on the next line
            chapter_title = None

            if i + 1 < len(lines):

                next_line = lines[i + 1]

                if (
                    not is_part(next_line)
                    and not is_chapter(next_line)
                    and not is_section(next_line)
                ):
                    chapter_title = next_line
                    i += 1

            i += 1
            continue

        # ====================================================
        # SECTION
        # ====================================================

        section_match = SECTION_PATTERN.match(line)

        if section_match:

            # Save previous section
            if section_number is not None:

                chunks.append(
                    create_chunk(
                        source,
                        part_number,
                        part_title,
                        chapter_number,
                        chapter_title,
                        section_number,
                        section_title,
                        section_lines
                    )
                )

            # -----------------------------------------------
            # Start new section
            # -----------------------------------------------

            section_number = section_match.group(1)

            # Text after the number and period
            title_on_same_line = section_match.group(2).strip()

            section_lines = [line]

            # ------------------------------------------------
            # Case 1:
            #
            # 308. Statute of limitation:
            #
            # ------------------------------------------------

            if title_on_same_line:

                section_title = title_on_same_line

            # ------------------------------------------------
            # Case 2:
            #
            # 1.
            # Short title and commencement:
            #
            # ------------------------------------------------

            else:

                section_title = None

                if i + 1 < len(lines):

                    next_line = lines[i + 1]

                    if (
                        not is_part(next_line)
                        and not is_chapter(next_line)
                        and not is_section(next_line)
                    ):

                        section_title = next_line

                        section_lines.append(next_line)

                        i += 1

            i += 1
            continue

        # ====================================================
        # NORMAL CONTENT
        # ====================================================

        if section_number is not None:

            section_lines.append(line)

        i += 1

    # ========================================================
    # SAVE LAST SECTION
    # ========================================================

    if section_number is not None:

        chunks.append(
            create_chunk(
                source,
                part_number,
                part_title,
                chapter_number,
                chapter_title,
                section_number,
                section_title,
                section_lines
            )
        )

    return chunks


# ============================================================
# PROCESS ONE FILE
# ============================================================

def process_file(file_name, source):
    """Read and parse one processed legal document."""

    input_path = PROCESSED_DIR / file_name

    if not input_path.exists():

        print(f"Missing file: {input_path}")

        return []

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = parse_document(text,source)

    print(f"{source}: " f"{len(chunks)} sections created")

    return chunks


def main():

    output_file = CHUNKS_DIR / "chunks.jsonl"

    all_chunks = []

    # Process all documents
    for file_name, source in FILES.items():

        chunks = process_file(file_name,source)
        all_chunks.extend(chunks)

    # ========================================================
    # WRITE JSONL
    # ========================================================

    with open(output_file, "w", encoding="utf-8") as file:
        for chunk in all_chunks:
            json.dump(chunk,file,ensure_ascii=False)
            file.write("\n")

    print()
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()