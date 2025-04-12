from langgraph.graph import StateGraph, START, END
from agents.input_analyzer_agent import analyze_node
from agents.research_agent import research_node
from agents.script_agent import script_node
from agents.rag_search_agent import rag_search_node
from agents.rag_script_agent import rag_script_node

def build_workflow():
    builder = StateGraph(dict)
    
    # Start with input analysis
    builder.add_edge(START, "analyze")
    builder.add_node("analyze", analyze_node)
    
    # Pipeline 1: Traditional research and script generation
    builder.add_edge("analyze", "research")
    builder.add_node("research", research_node)
    builder.add_edge("research", "script")
    builder.add_node("script", script_node)
    builder.add_edge("script", END)
    
    # Pipeline 2: RAG-based retrieval and script generation
    builder.add_edge("analyze", "rag_search")
    builder.add_node("rag_search", rag_search_node)
    builder.add_edge("rag_search", "rag_script")
    builder.add_node("rag_script", rag_script_node)
    builder.add_edge("rag_script", END)
    
    return builder.compile()
