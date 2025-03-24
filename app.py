# app.py

import streamlit as st
import time
import os
from core.coordinator import build_workflow
import openai
from tools.text_to_speech import generate_speech

# Load OpenAI API key from Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
elif "openai_api_key" in st.secrets:
    openai.api_key = st.secrets["openai_api_key"]

def main():
    st.title("AI-Driven Podcast Script Generator")
    
    topics = st.text_input("Enter topic(s)", value="RAG, Fine-tuning, Vector Databases")
    direction = st.text_area(
        "Enter podcast instructions",
        value="Explain how these technologies impact AI careers.",
    )

    if st.button("Generate Script & Audio"):
        st.info("Generating script...")
        time.sleep(1)  # Simulate delay for visual effect.

        workflow = build_workflow()
        state = {
            "topics": topics,
            "direction": direction,
            "speaker_style": "One speaker",  # Hardcoded to one speaker
        }
        final_state = workflow.invoke(state)
        script_output = final_state.get("script_output", "No script generated.")

        st.write("Generated Script:")
        st.text_area("", value=script_output, height=300)
        
        # Convert text to speech
        if openai.api_key:
            st.info("Converting script to audio...")
            audio_path = generate_speech(script_output)
            
            if audio_path:
                st.success("Audio generated successfully!")
                st.write("Listen to your podcast:")
                st.audio(audio_path)
            else:
                st.error("Failed to generate audio. Please check the API key in your .streamlit/secrets.toml file.")
        else:
            st.error("OpenAI API key not found in Streamlit secrets. Please add it to your .streamlit/secrets.toml file as OPENAI_API_KEY or openai_api_key.")


if __name__ == "__main__":
    main()
