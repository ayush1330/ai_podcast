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

    topics = st.text_input("Enter topic(s)", value="")
    direction = st.text_area(
        "Enter podcast instructions",
        value="",
    )

    # Add dropdown for knowledge level
    knowledge_level = st.selectbox(
        "Select knowledge level about the topic",
        options=["beginner", "intermediate", "expert"],
    )

    # Add dropdown for desired outcome
    desired_outcome = st.selectbox(
        "Select desired outcome",
        options=["entertainment", "learning", "inspiration", "problem-solving"],
    )

    # Add dropdown for preferred podcast length
    preferred_length = st.selectbox(
        "Select preferred podcast length",
        options=["1 min", "2 mins", "3 mins"],
    )

    # Add dropdown for format preferences
    format_preference = st.selectbox(
        "Select format preference",
        options=["storytelling", "Q&A", "deep dive analysis"],
    )

    if st.button("Generate Script & Audio"):
        st.info("Generating script...")
        time.sleep(1)  # Simulate delay for visual effect.

        workflow = build_workflow()
        state = {
            "topics": topics,
            "direction": direction,
            "speaker_style": "One speaker",  # Hardcoded to one speaker
            "knowledge_level": knowledge_level,  # Add knowledge level to state
            "desired_outcome": desired_outcome,  # Add desired outcome to state
            "preferred_length": preferred_length,  # Add preferred length to state
            "format_preference": format_preference,  # Add format preference to state
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
                st.error(
                    "Failed to generate audio. Please check the API key in your .streamlit/secrets.toml file."
                )
        else:
            st.error(
                "OpenAI API key not found in Streamlit secrets. Please add it to your .streamlit/secrets.toml file as OPENAI_API_KEY or openai_api_key."
            )


if __name__ == "__main__":
    main()
