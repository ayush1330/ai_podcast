# app.py

import streamlit as st
import time
import os
from core.coordinator import build_workflow
from fpdf import FPDF
import unicodedata


def save_script_to_pdf(script_text: str, filename: str = "podcast_script.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Clean text of problematic Unicode characters
    def clean_text(text):
        # Replace smart quotes with regular quotes
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        # Replace other common Unicode characters
        text = text.replace("\u2013", "-").replace("\u2014", "--")
        text = text.replace("\u2026", "...")
        return text

    # Apply text cleaning
    cleaned_text = clean_text(script_text)

    # Process by line
    for line in cleaned_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    if not os.path.exists("scripts"):
        os.makedirs("scripts")
    pdf_path = os.path.join("scripts", filename)
    pdf.output(pdf_path)
    return pdf_path


def main():
    st.title("AI-Driven Podcast Script Generator")
    topics = st.text_input("Enter topic(s)", value="RAG, Fine-tuning, Vector Databases")
    direction = st.text_area(
        "Enter podcast instructions",
        value="Explain how these technologies impact AI careers.",
    )
    speaker_style = st.selectbox("Number of speakers", ["One speaker", "Two speakers"])

    if st.button("Generate Script & Save as PDF"):
        st.info("Generating script...")
        time.sleep(1)  # Simulate delay for visual effect.

        workflow = build_workflow()
        state = {
            "topics": topics,
            "direction": direction,
            "speaker_style": speaker_style,
        }
        final_state = workflow.invoke(state)
        script_output = final_state.get("script_output", "No script generated.")

        pdf_path = save_script_to_pdf(script_output)
        st.success("Done")
        st.write("Generated Script:")
        st.text_area("", value=script_output, height=300)
        st.write(f"Script saved as PDF: {pdf_path}")


if __name__ == "__main__":
    main()
