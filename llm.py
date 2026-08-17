import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_documents(transcript_pages, notes_pages, workbook_data):

    # -------------------------
    # Build Transcript Text
    # -------------------------

    transcript_text = ""

    if isinstance(transcript_pages, str):
        transcript_text = transcript_pages

    else:
        for page in transcript_pages:

            if isinstance(page, dict):
                transcript_text += (
                    f"\n\n--- TRANSCRIPT PAGE {page.get('page')} ---\n"
                )
                transcript_text += page.get("text", "")

            else:
                transcript_text += str(page)

    # -------------------------
    # Build Notes Text
    # -------------------------

    notes_text = ""

    if notes_pages:

        if isinstance(notes_pages, str):
            notes_text = notes_pages

        else:
            for page in notes_pages:

                if isinstance(page, dict):
                    notes_text += (
                        f"\n\n--- NOTES PAGE {page.get('page')} ---\n"
                    )
                    notes_text += page.get("text", "")

                else:
                    notes_text += str(page)

    # -------------------------
    # Build Workbook Text
    # -------------------------

    workbook_text = ""

    if isinstance(workbook_data, str):

        workbook_text = workbook_data

    elif isinstance(workbook_data, list):

        for sheet in workbook_data:

            if not isinstance(sheet, dict):
                continue

            workbook_text += (
                f"\n\n=====================\n"
                f"SHEET : {sheet.get('sheet')}\n"
                f"=====================\n"
            )

            cells = sheet.get("cells", [])

            for cell in cells:

                if not isinstance(cell, dict):
                    continue

                workbook_text += (
                    f"Cell: {cell.get('cell')} | "
                    f"Value: {cell.get('value')} | "
                    f"Formula: {cell.get('formula')}\n"
                )

    else:

        workbook_text = str(workbook_data)

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
            You are a Senior Equity Research Analyst.

            You have been given:

            1. Earnings Call Transcript
            2. Hedge Fund / Analyst Notes
            3. Financial Model

            Your task is NOT to modify the financial model.

            Instead, determine which cells are MOST LIKELY to require updates based on management guidance.

            Rules:

            - NEVER suggest changing historical values.
            - ONLY suggest forecast or assumption cells.
            - Explain WHY each cell is impacted.
            - Mention transcript page numbers.
            - If an impact is due to formulas, write "Derived".

            Return ONLY a markdown table.

            Columns:

            | Sheet | Cell | Metric | Why Impacted | Transcript Page | Confidence |

            Transcript:

            {transcript_text[:40000]}

            Notes:

            {notes_text[:15000]}

            Financial Model:

            {workbook_text[:35000]}
            """

    response = model.generate_content(prompt)

    return response.text