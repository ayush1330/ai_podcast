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
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", api_key=OPENAI_API_KEY)
    template = "Research and summarize the following topics: {topics}."
    prompt = PromptTemplate(input_variables=["topics"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def create_script_chain():
    """
    Creates an LLMChain for the script generation agent.
    It uses a prompt template that combines research output, instructions, and speaker style to generate a podcast script.
    """
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", api_key=OPENAI_API_KEY)
    template = (
        "Using the following research output: {research_output}\n"
        "and the following instructions: {direction}\n"
        "and the speaker style: {speaker_style}\n"
        "Generate a well-structured and engaging podcast script."
    )
    prompt = PromptTemplate(
        input_variables=["research_output", "direction", "speaker_style"],
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
