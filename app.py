import streamlit as st
from parser import extract_pdf_text
from excel_parser import extract_excel_data
from llm import analyze_documents

st.set_page_config(page_title="Financial Model Impact Analyzer")

st.title("📈 Financial Model Impact Analyzer")

transcript = st.file_uploader(
    "Upload Earnings Call Transcript",
    type=["pdf"]
)

notes = st.file_uploader(
    "Upload Analyst / Hedge Fund Notes (Optional)",
    type=["pdf"]
)

excel = st.file_uploader(
    "Upload Financial Model",
    type=["xlsx", "xlsm"]
)


if st.button("Analyze"):

    if transcript and notes and excel:

        with st.spinner("Reading documents..."):

            transcript_text = extract_pdf_text(transcript)
            notes_text = extract_pdf_text(notes)
            excel_text = extract_excel_data(excel)

            st.write("===== DEBUG =====")

            st.write("Transcript Type:", type(transcript_text))
            st.write("Transcript First Item:")
            st.write(transcript_text[0])

            st.write("Notes Type:", type(notes_text))
            st.write("Notes First Item:")
            st.write(notes_text[0])

            st.write("Excel Type:", type(excel_text))
            st.write("Excel First Item:")
            st.write(excel_text[0])

        with st.spinner("Analyzing with Gemini..."):

            result = analyze_documents(
                transcript_text,
                notes_text,
                excel_text
            )

        st.success("Analysis Complete!")

        st.write(result)

    else:

        st.error("Please upload all three files.")