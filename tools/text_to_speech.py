import os
from datetime import datetime
import openai

def generate_speech(text, output_dir="audio"):
    """
    Convert text to speech using OpenAI's TTS API
    
    Args:
        text (str): The text to convert to speech
        output_dir (str): Directory to save the audio file
        
    Returns:
        str: Path to the generated audio file or None if there was an error
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"podcast_{timestamp}.mp3")
    
    try:
        # Using OpenAI TTS
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(output_path)
        
        print(f"Audio saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None 