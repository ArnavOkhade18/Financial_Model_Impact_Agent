# Financial Model Impact Agent

## Overview

Financial Model Impact Agent is an AI-powered financial analysis tool that helps equity research analysts identify which forecast assumptions and financial model cells are likely impacted after an earnings call.

Instead of modifying the financial model, the application recommends which cells should be reviewed, explains why, and cites supporting evidence from the earnings call transcript.

---

## Features

- Upload Earnings Call Transcript (PDF)
- Upload Hedge Fund / Analyst Notes (PDF)
- Upload Financial Model (Excel)
- AI identifies impacted forecast cells
- Explains reasoning behind every recommendation
- References transcript pages
- Does **not** modify the Excel model

---

## Tech Stack

- Python
- Streamlit
- Google Gemini 2.5 Flash
- PyMuPDF
- OpenPyXL

---

## Future Improvements

- Formula dependency tracing
- Multi-agent workflow
- Retrieval-Augmented Generation (RAG)
- Excel visualization
- Confidence scoring
