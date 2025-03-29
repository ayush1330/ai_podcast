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

# Configure the Streamlit page
st.set_page_config(
    page_title="Personalized Podcast with Your Host AI",
    page_icon="🎙",
    layout="wide",
)

# Inject custom CSS
st.markdown(
    """
    <style>
    /* Import a modern Google Font (Poppins) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* Global settings */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #1F1F1F;
        color: #E0E0E0;
        margin: 0;
        padding: 0;
    }

    /* Main Streamlit container adjustments */
    .stApp {
        background-color: #1F1F1F;
        padding: 1rem 2rem;
    }

    /* Heading styles */
    .main-heading {
        font-size: 2rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 0;
    }
    .subheading {
        color: #BDBDBD;
        font-size: 1rem;
        margin: 0.1rem 0 0.1rem 0;
    }

    /* A thin horizontal line */
    .thin-line {
        border: none;
        border-bottom: 1px solid #666666;
        margin: 0.1rem 0;
        width: 100%;
    }

    /* Form labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #E0E0E0 !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #9C27B0;
        color: #FFFFFF;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #7B1FA2;
    }

    /* Info, success, error boxes styling */
    .stAlert {
        border-radius: 8px;
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #424242;
    }

    /* Column spacing for clarity */
    .css-1inhoud, .css-1kyxreq {
        gap: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    # Minimal heading
    st.markdown(
        "<h1 class='main-heading'>Personalized Podcast with Your Host AI 🎙️ </h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subheading'>Generate custom, AI-driven podcast tailored to your needs.</p>",
        unsafe_allow_html=True,
    )

    # A thin, light-grey line
    st.markdown("<hr class='thin-line' />", unsafe_allow_html=True)

    # Card container for form
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Text input for topics
            topics = st.text_area("Enter topic(s)", value="")
            # Text area for additional instructions
            direction = st.text_area("Enter podcast instructions", value="")

        with col2:
            # Knowledge level dropdown
            knowledge_level = st.selectbox(
                "Select knowledge level about the topic",
                options=["beginner", "intermediate", "expert"],
            )
            # Desired outcome dropdown
            desired_outcome = st.selectbox(
                "Select desired outcome",
                options=["entertainment", "learning", "inspiration", "problem-solving"],
            )
            # Preferred podcast length
            preferred_length = st.selectbox(
                "Select preferred podcast length",
                options=["1 min", "2 mins", "3 mins"],
            )
            # Format preference
            format_preference = st.selectbox(
                "Select format preference",
                options=["storytelling", "Q&A", "deep dive analysis"],
            )

            # The "Generate Script & Audio" button is now placed here (further up)
            generate_button = st.button("Generate Script & Audio")

        st.markdown("</div>", unsafe_allow_html=True)

    # Trigger generation if the button was clicked
    if generate_button:
        st.info("Generating script...")
        time.sleep(1)  # Simulate delay for visual effect

        # Invoke your workflow
        workflow = build_workflow()
        state = {
            "topics": topics,
            "direction": direction,
            "speaker_style": "One speaker",  # Hardcoded to one speaker
            "knowledge_level": knowledge_level,
            "desired_outcome": desired_outcome,
            "preferred_length": preferred_length,
            "format_preference": format_preference,
        }
        final_state = workflow.invoke(state)
        script_output = final_state.get("script_output", "No script generated.")

        st.write("**Generated Script:**")
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
                    "Failed to generate audio. Please check your API key settings."
                )
        else:
            st.error(
                "OpenAI API key not found. Please configure it in `.streamlit/secrets.toml`."
            )


if __name__ == "__main__":
    main()
