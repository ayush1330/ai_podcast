# agents/research_agent.py

from core.agent_factory import create_research_chain
from langgraph.types import Command


def research_node(state: dict) -> Command:
    """
    Research agent node: uses the research chain to generate research output.
    Reads the 'topics' field from state and updates state with 'research_output'.
    """
    topics = state.get("topics", "")
    research_chain = create_research_chain()
    # Run the chain with the topics input.
    research_output = research_chain.run(topics=topics)
    state["research_output"] = research_output.strip()
    print("Research Agent Output:", state["research_output"])
    # Move to next node ("script")
    return Command(update=state, goto="script")
