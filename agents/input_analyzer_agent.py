# agents/input_analyzer_agent.py

from core.agent_factory import create_input_analyzer_chain
from langgraph.types import Command


def analyze_node(state: dict) -> Command:
    """
    Input analyzer agent node: analyzes user inputs to enhance topics and directions.
    Reads the 'topics' and 'direction' fields from state and updates with improved versions.
    """
    topics = state.get("topics", "")
    direction = state.get("direction", "")
    knowledge_level = state.get(
        "knowledge_level", ""
    )  # Get knowledge level with default
    desired_outcome = state.get(
        "desired_outcome", ""
    )  # Get desired outcome with default
    preferred_length = state.get(
        "preferred_length", ""
    )  # Get preferred length with default
    format_preference = state.get(
        "format_preference", ""
    )  # Get format preference with default

    input_analyzer_chain = create_input_analyzer_chain()
    # Run the chain with the inputs.
    analysis_result = input_analyzer_chain.run(
        topics=topics,
        direction=direction,
        knowledge_level=knowledge_level,
        desired_outcome=desired_outcome,
        preferred_length=preferred_length,
        format_preference=format_preference,
    )

    # Parse analysis results
    # Assuming the LLM returns a formatted string with sections for enhanced_topics and enhanced_direction
    lines = analysis_result.strip().split("\n")
    enhanced_topics = topics
    enhanced_direction = direction

    for i, line in enumerate(lines):
        if line.startswith("ENHANCED_TOPICS:"):
            enhanced_topics = lines[i + 1].strip()
        elif line.startswith("ENHANCED_DIRECTION:"):
            enhanced_direction = lines[i + 1].strip()

    # Update state with enhanced inputs
    state["topics"] = enhanced_topics
    state["direction"] = enhanced_direction
    state["input_analysis"] = analysis_result.strip()

    print("Input Analyzer Output:", state["input_analysis"])
    # Move to next node ("research")
    return Command(update=state, goto="research")
