# core/agent_factory.py

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from core.settings import OPENAI_API_KEY


def create_research_chain():
    """
    Creates an LLMChain for the research agent.
    It uses a prompt template to instruct the LLM to research and summarize topics.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
    template = (
        "Conduct a deep research on the following topics: {topics}.\n "
        "Include real-world examples, case studies, and statistics to provide a comprehensive understanding.\n"
        "The audience's knowledge level about this topic is: {knowledge_level}. \n"
        "Tailor your research depth and complexity accordingly.\n\n"
    )
    prompt = PromptTemplate(
        input_variables=["topics", "knowledge_level"], template=template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def create_rag_search_chain():
    """
    Creates an LLMChain for the RAG search agent.
    The prompt uses 'topics', 'direction', and 'raw_context' as inputs.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
    template = (
        "Conduct a deep research on the following topics: {topics}.\n "
        "Conduct a deep research on the Raw Retrieved Context: {raw_context}\n"
        "Include real-world examples, case studies, and statistics to provide a comprehensive understanding. "
        "The audience's knowledge level about this topic is: {knowledge_level}. \n"
        "Tailor your research depth and complexity accordingly."
        "Follow the direction in which user want their podcast to be: {direction}\n\n"
    )
    prompt = PromptTemplate(
        input_variables=["topics", "raw_context", "knowledge_level", "direction"],
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def create_input_analyzer_chain():
    """
    Creates an LLMChain for the input analyzer agent.
    It uses a prompt template to analyze and enhance the user's topics and directions.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
    template = (
        "Analyze the following podcast topics and instructions to enhance them for better research and script generation.\n\n"
        "Topics: {topics}\n"
        "Instructions: {direction}\n"
        "Audience Knowledge Level: {knowledge_level}\n"
        "Desired Outcome: {desired_outcome}\n"
        "Preferred Length: {preferred_length}\n"
        "Format Preference: {format_preference}\n\n"
        "Your task is to:\n"
        "1. Expand vague topics into more specific, researchable areas\n"
        "2. Clarify ambiguous instructions\n"
        "3. Add relevant angles or perspectives that might be valuable\n"
        "4. Consider the listener demographics: age group 18-28, professional background in AI, education level of Masters and Bachelors students\n"
        "5. Ensure the content tone is engaging and educational\n"
        "6. Include real-world examples, case studies, or statistics where applicable\n"
        "7. Adjust complexity and depth based on the audience's knowledge level\n"
        "8. Tailor content to achieve the desired outcome ({desired_outcome})\n"
        "9. Structure content appropriately for the preferred format ({format_preference})\n"
        "10. Optimize content for the specified duration ({preferred_length})\n\n"
        "Return your analysis in the following format:\n"
        "ENHANCED_TOPICS:\n[enhanced topics here]\n"
        "ENHANCED_DIRECTION:\n[enhanced directions here]\n"
        "ANALYSIS:\n[brief explanation of your understanding of what user wants]"
    )
    prompt = PromptTemplate(
        input_variables=[
            "topics",
            "direction",
            "knowledge_level",
            "desired_outcome",
            "preferred_length",
            "format_preference",
        ],
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def create_script_chain():
    """
    Creates an LLMChain for the RAG script generation agent.
    This chain constructs a prompt that includes the original inputs (topics, direction, speaker style, knowledge level,
    desired outcome, preferred length, format preference) along with the refined retrieved context.
    The prompt instructs the LLM to generate a well-structured, engaging podcast script that integrates the extra
    retrieved details to enrich the content.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
    template = (
        "Using the following research output: {research_output}\n"
        "and the following instructions: {direction}\n"
        "and the speaker style: {speaker_style}\n"
        "and considering the audience knowledge level: {knowledge_level}\n"
        "and the desired outcome: {desired_outcome}\n"
        "and the preferred length: {preferred_length}\n"
        "and the format preference: {format_preference}\n"
        "Generate a well-structured and engaging podcast script.\n\n"
        "IMPORTANT TONE AND STYLE GUIDELINES:\n"
        "- This is a PODCAST script meant to be SPOKEN, not read\n"
        "- Use natural, conversational language with a warm, engaging tone\n"
        "- Include brief pauses, emphasis, and natural speech patterns\n"
        "- Speak directly to the listener as if having a conversation\n"
        '- Use rhetorical questions, personal anecdotes, and direct address ("you")\n'
        "- Add personality, energy, and enthusiasm to make it sound like a real podcast\n"
        "- Incorporate verbal transitions, signposting, and vocal variety\n\n"
        "REQUIRED STRUCTURE:\n"
        "1. START WITH: A welcoming introduction that includes \"Hello and welcome! I'm your host Jane\" followed by a brief overview of today's topic\n"
        "2. MAIN CONTENT: Develop the topic with explanations, examples, and insights\n"
        "3. END WITH: A motivational conclusion that encourages listeners to explore the topic further and sparks curiosity\n\n"
        "IMPORTANT FORMATTING INSTRUCTIONS:\n"
        "1. DO NOT include 'Podcast Script:' at the beginning\n"
        "2. DO NOT include 'Host:' or any speaker labels in the script\n"
        "3. Focus on creating a script that sounds natural when spoken aloud\n\n"
        "The script should be tailored for university students in the field of AI, making them more curious to learn.\n"
        "Incorporate real-world examples, case studies, or statistics to enhance the educational value.\n"
        "Adjust the complexity, terminology, and depth of explanations based on the audience's knowledge level.\n"
        "Structure the content to achieve the specified outcome ({desired_outcome}).\n"
        "Format the script according to the preferred style ({format_preference}).\n\n"
        "IMPORTANT LENGTH REQUIREMENTS (DO NOT INCLUDE THIS IN OUTPUT):\n"
        "- For 1 min podcast: 150 words maximum\n"
        "- For 2 mins podcast: 300 words maximum\n"
        "- For 3 mins podcast: 450 words maximum\n"
        "Your script for {preferred_length} MUST strictly adhere to these word count limits.\n"
        "Count your words carefully before finalizing the script but DO NOT include the word count in the output."
    )
    prompt = PromptTemplate(
        input_variables=[
            "research_output",
            "direction",
            "speaker_style",
            "knowledge_level",
            "desired_outcome",
            "preferred_length",
            "format_preference",
        ],
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def create_rag_script_chain():
    """
    Creates an LLMChain for the script generation agent.
    It uses a prompt template that combines research output, instructions, and speaker style to generate a podcast script.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
    template = (
        "Using the following research output: {refined_context}\n"
        "Create an informative script which uses up to date information from {refined_context}\n"
        "and the following instructions: {direction}\n"
        "and the speaker style: {speaker_style}\n"
        "and considering the audience knowledge level: {knowledge_level}\n"
        "and the desired outcome: {desired_outcome}\n"
        "and the preferred length: {preferred_length}\n"
        "and the format preference: {format_preference}\n"
        "Generate a well-structured and engaging podcast script.\n\n"
        "IMPORTANT TONE AND STYLE GUIDELINES:\n"
        "- This is a PODCAST script meant to be SPOKEN, not read\n"
        "- Use natural, conversational language with a warm, engaging tone\n"
        "- Include brief pauses, emphasis, and natural speech patterns\n"
        "- Speak directly to the listener as if having a conversation\n"
        '- Use rhetorical questions, personal anecdotes, and direct address ("you")\n'
        "- Add personality, energy, and enthusiasm to make it sound like a real podcast\n"
        "- Incorporate verbal transitions, signposting, and vocal variety\n\n"
        "REQUIRED STRUCTURE:\n"
        "1. START WITH: A welcoming introduction that includes \"Hello and welcome! I'm your host Jane\" followed by a brief overview of today's topic\n"
        "2. MAIN CONTENT: Develop the topic with explanations, examples, and insights\n"
        "3. END WITH: A motivational conclusion that encourages listeners to explore the topic further and sparks curiosity\n\n"
        "IMPORTANT FORMATTING INSTRUCTIONS:\n"
        "1. DO NOT include 'Podcast Script:' at the beginning\n"
        "2. DO NOT include 'Host:' or any speaker labels in the script\n"
        "3. Focus on creating a script that sounds natural when spoken aloud\n\n"
        "The script should be tailored for university students in the field of AI, making them more curious to learn.\n"
        "Incorporate real-world examples, case studies, or statistics to enhance the educational value.\n"
        "Adjust the complexity, terminology, and depth of explanations based on the audience's knowledge level.\n"
        "Structure the content to achieve the specified outcome ({desired_outcome}).\n"
        "Format the script according to the preferred style ({format_preference}).\n\n"
        "IMPORTANT LENGTH REQUIREMENTS (DO NOT INCLUDE THIS IN OUTPUT):\n"
        "- For 1 min podcast: 150 words maximum\n"
        "- For 2 mins podcast: 300 words maximum\n"
        "- For 3 mins podcast: 450 words maximum\n"
        "Your script for {preferred_length} MUST strictly adhere to these word count limits.\n"
        "Count your words carefully before finalizing the script but DO NOT include the word count in the output."
    )
    prompt = PromptTemplate(
        input_variables=[
            "refined_context",
            "direction",
            "speaker_style",
            "knowledge_level",
            "desired_outcome",
            "preferred_length",
            "format_preference",
        ],
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
