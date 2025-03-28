# AI Podcast Generator 🎙️

A powerful AI-powered podcast generation system that creates personalized podcast content using advanced language models and text-to-speech technology. This project leverages Streamlit for the user interface and integrates various AI components to create engaging podcast content.

## Features 🌟

- **Interactive Web Interface**: Built with Streamlit for a user-friendly experience
- **AI-Powered Content Generation**: Utilizes OpenAI's language models for content creation
- **Text-to-Speech Integration**: Converts generated content into natural-sounding speech
- **Modular Architecture**: Organized into core components, agents, and tools
- **Environment Variable Support**: Secure API key management
- **Modern UI Design**: Clean and responsive interface with custom styling

## Prerequisites 📋

- Python 3.10 or higher
- OpenAI API key
- Virtual environment (recommended)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai_podcast.git
cd ai_podcast
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage 💡

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter your preferences and requirements in the web interface

4. Click the generate button to create your personalized podcast

## Project Structure 📁

```
ai_podcast/
├── agents/           # AI agent implementations
├── audio/           # Generated audio files
├── core/            # Core functionality and workflows
├── tools/           # Utility tools and functions
├── app.py           # Main Streamlit application
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## Dependencies 📦

- streamlit: Web interface framework
- openai: OpenAI API integration
- langchain: Language model framework
- llama-index: Document processing
- chromadb: Vector database
- fpdf: PDF generation
- langgraph: Workflow management
- And more (see requirements.txt)

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- OpenAI for their powerful language models
- Streamlit for the web framework
- All contributors and maintainers of the open-source libraries used in this project 
