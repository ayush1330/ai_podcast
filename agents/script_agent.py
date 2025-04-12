import os
import re
import datetime
from core.agent_factory import create_script_chain
from langgraph.types import Command
from langgraph.graph import END


def sanitize_filename(filename: str) -> str:
    """
    Remove or replace characters not allowed in Windows file names.
    """
    # Remove characters: < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', "", filename)


def script_node(state: dict) -> Command:
    """
    Script generation agent node (Pipeline 1):
    Uses the script chain to generate the podcast script by combining research output,
    podcast instructions, and other parameters. The generated script is then saved to the
    "llm_script" folder with a unique filename.
    """
    research_output = state.get("research_output", "")
    direction = state.get("direction", "")
    speaker_style = state.get("speaker_style", "")
    knowledge_level = state.get("knowledge_level", "")
    desired_outcome = state.get("desired_outcome", "")
    preferred_length = state.get("preferred_length", "")
    topics = state.get("topics", "")

    # Create and run the script generation chain
    script_chain = create_script_chain()
    script_output = script_chain.run(
        research_output=research_output,
        direction=direction,
        speaker_style=speaker_style,
        knowledge_level=knowledge_level,
        desired_outcome=desired_outcome,
        preferred_length=preferred_length,
        format_preference=state.get("format_preference", ""),
        topics=topics,
    )
    state["script_output"] = script_output.strip()
    print("Script Agent Output:", state["script_output"])

    # Save the generated script to the "llm_script" folder
    output_folder = "llm_script"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Replace spaces and sanitize the topic to make a safe file name
    topic_slug = sanitize_filename(topics.strip().replace(" ", "_"))[:30]
    filename = f"podcast_{timestamp}_{topic_slug}.txt"
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script_output)
    state["script_file"] = output_path
    print("Script saved to:", output_path)

    # Return a Command object to move to the END node
    return Command(update=state, goto=END)
