import os
import re
import datetime
from core.agent_factory import create_rag_script_chain
from langgraph.types import Command
from langgraph.graph import END


def sanitize_filename(filename: str) -> str:
    """
    Remove characters not allowed in Windows file names.
    """
    # Remove characters: < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', "", filename)


def rag_script_node(state: dict) -> Command:
    """
    Pipeline 2: Script generation agent for the RAG branch.
    This function extracts the refined retrieved context along with other user inputs,
    constructs an enriched prompt using the LLM chain created via create_rag_script_chain(),
    generates the final podcast script, saves it in the "rag_script" folder, and returns a Command.
    """
    # Extract inputs from the state
    refined_context = state.get("refined_context", "")
    direction = state.get("direction", "")
    speaker_style = state.get("speaker_style", "")
    knowledge_level = state.get("knowledge_level", "")
    desired_outcome = state.get("desired_outcome", "")
    preferred_length = state.get("preferred_length", "")
    format_preference = state.get("format_preference", "")
    topics = state.get("topics", "")

    # Create the LLM chain for generating the script tailored for RAG
    rag_script_chain = create_rag_script_chain()

    # Run the chain with all required inputs, including the retrieved context
    script_output = rag_script_chain.run(
        refined_context=refined_context,
        direction=direction,
        speaker_style=speaker_style,
        knowledge_level=knowledge_level,
        desired_outcome=desired_outcome,
        preferred_length=preferred_length,
        format_preference=format_preference,
        topics=topics,
    )

    # Save the generated script to the "rag_script" folder with a unique, sanitized filename
    output_folder = "rag_script"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Replace spaces with underscores and sanitize the topic slug
    topic_slug = sanitize_filename(topics.strip().replace(" ", "_"))[:30]
    filename = f"podcast_{timestamp}_{topic_slug}.txt"
    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script_output)

    # Update the state with the generated script output and file path
    state["rag_script_output"] = script_output.strip()
    state["rag_script_file"] = output_path

    print("RAG Script Agent Output:", state["rag_script_output"])
    print("Script saved to:", output_path)

    # Return a Command object to signal the end of this branch
    return Command(update=state, goto=END)
