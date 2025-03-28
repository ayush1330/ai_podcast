# core/coordinator.py
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from agents.input_analyzer_agent import analyze_node
from agents.research_agent import research_node
from agents.script_agent import script_node


def build_workflow():
    builder = StateGraph(dict)
    builder.add_edge(START, "analyze")
    builder.add_node("analyze", analyze_node)
    builder.add_edge("analyze", "research")
    builder.add_node("research", research_node)
    builder.add_edge("research", "script")
    builder.add_node("script", script_node)
    builder.add_edge("script", END)
    return builder.compile()
