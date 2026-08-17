import fitz

def extract_pdf_text(pdf_file):

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page_num, page in enumerate(pdf):

        page_text = page.get_text()

        text += f"\n\n--- PAGE {page_num + 1} ---\n"

        text += page_text

    return text