from pathlib import Path

import chromadb
import pdfplumber
from pdfplumber.page import Page
from sentence_transformers import SentenceTransformer

full_time_path = str(Path(__file__).parent.parent / "storage/full_time_programs.pdf")
schools = []
programmes: list[dict] = []


def get_full_time_programmes():
    """Retrieves a list of programmes from the PDF file
    """
    with pdfplumber.open(full_time_path) as pdf:
        # Iterate through pages
        for page in pdf.pages:
            current_school = get_school_title(page)
            tables = page.extract_tables()

            # If title exists
            if current_school:
                # Add the new school to the list
                schools.append(current_school)

                # If two tables exist in the current page
                if len(tables) == 2:
                    # The first table belongs to the previous school
                    process_table(tables[0], schools[-2])
                    # The second table belongs to the current school
                    process_table(tables[1], current_school)
                else:
                    process_table(tables[0], current_school)
            # If no title exists all tables belong to the last appended school
            else:
                for table in tables:
                    process_table(table, schools[-1])


def get_school_title(page: Page) -> str | None:
    """Detects if a title exists in a page

    :param page: PDF page
    :return: The title or None
    """
    lines = page.extract_text().splitlines()

    for line in lines:
        if line.startswith("SCHOOL OF"):
            return line.strip()
    return None


def process_table(table, school: str):
    """Extracts programme details from a table to a dictionary

    :param table: PDF table
    :param school: The school the table belongs to
    :return:
    """
    for row in table:
        if len(row) != 4 or row[0].lower() == "programme":
            continue

        programme, requirements, campus, fee = row

        details = {
            "programme": programme.replace('\n', ' '),
            "school": school,
            "requirements": requirements.replace('\n', ' '),
            "campus": campus.replace('\n', 'or'),
            'fee': fee.replace('\n', ' ')
        }

        programmes.append(details)


def clean_output():
    merged = []
    skip_next = False

    for i in range(len(programmes)):
        # Check if the current object is to be skipped
        if skip_next:
            skip_next = False
            continue

        current = programmes[i]

        # Check if the next object is the continuation of the current one
        if i + 1 < len(programmes):
            nxt = programmes[i + 1]

            if nxt["campus"] == "" and nxt["fee"] == "":
                # Merge fields
                current["programme"] = (
                    (current["programme"] + " " + nxt["programme"]).strip()
                )
                current["requirements"] = (
                    (current["requirements"] + " " + nxt["requirements"]).strip()
                )
                skip_next = True
        merged.append(current)
    return merged


get_full_time_programmes()

chunks = []

# Convert text to chunks for embedding
for p in programmes:
    text = (
        f"Programme: {p['programme']}\n"
        f"School: {p['school']}\n"
        f"Requirements: {p['requirements']}\n"
        f"Campus: {p['campus']}\n"
        f"Fee: {p['fee']}\n"
    )

    chunks.append(text)

model = SentenceTransformer("sentence-transformers/All-MiniLM-L6-V2")
embeddings = model.encode(chunks, convert_to_tensor=True).tolist()

client = chromadb.PersistentClient(path=str(Path(__file__).parent.parent / "storage/chromadb"))

# Remove collection if it exists to avoid duplications
try:
  client.delete_collection(name="full_time_programmes")
  print("Removed existing collection")
except Exception:
  pass

collection = client.get_or_create_collection(name="full_time_programmes")
ids = [f"programme_{course_id}" for course_id in range(len(chunks))]

collection.add(ids=ids, embeddings=embeddings, documents=chunks)

print("Data successfully embedded")
