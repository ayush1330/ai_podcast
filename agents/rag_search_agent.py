import os
import glob
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from core.agent_factory import create_rag_search_chain
from langgraph.types import Command
from langchain.utilities import SerpAPIWrapper
import streamlit as st

# Retrieve SerpAPI API key from secrets.toml via st.secrets
serpapi_key = st.secrets["SERPAPI_API_KEY"]


def get_web_search_summary(query: str) -> str:
    """
    Perform a web search using SerpAPI with the given query,
    process the results (using the built-in SerpAPI wrapper),
    and return a formatted summary text.
    """
    # Instantiate SerpAPIWrapper with your API key
    serpapi = SerpAPIWrapper(serpapi_api_key=serpapi_key)
    # Run the search; SerpAPIWrapper returns a text summary
    web_summary = serpapi.run(query)
    return web_summary


def rag_search_node(state: dict) -> Command:
    """
    Pipeline 2: Retrieval Agent for RAG.
    This node checks if a pre-built FAISS index exists in the "faiss_index" folder.
    - If it exists, it loads the index with dangerous deserialization enabled.
    - Otherwise, it reads PDFs from the "doc" folder, extracts text, splits it into chunks,
      builds the FAISS index, and saves it for future runs.
    Then it retrieves top matching documents based on the query,
    performs a web search to get up-to-date results,
    merges both sources into a combined context,
    refines the context with an LLM chain, updates the state, and moves to "rag_script".
    """
    index_path = "faiss_index"  # Folder where the pre-built index is stored
    # Initialize the embedding model
    embedding_model = OpenAIEmbeddings(disallowed_special=())

    # Check if the pre-built index exists
    if os.path.exists(index_path) and os.path.isdir(index_path):
        # Load the pre-built FAISS index from disk with dangerous deserialization enabled
        faiss_index = FAISS.load_local(
            index_path, embedding_model, allow_dangerous_deserialization=True
        )
        print("Loaded FAISS index from", index_path)
    else:
        # Step 1: Locate all PDF files in the "doc" folder
        pdf_files = glob.glob(os.path.join("doc", "*.pdf"))
        # Step 2: Extract text from each PDF
        full_text = ""
        for pdf_file in pdf_files:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        # Step 3: Split the full text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        chunks = text_splitter.split_text(full_text)
        # Step 4: Build the FAISS index from the chunks
        faiss_index = FAISS.from_texts(chunks, embedding_model)
        # Save the built index to disk for future runs
        faiss_index.save_local(index_path)
        print("Built and saved FAISS index to", index_path)

    # Step 5: Retrieve top matching documents using the query from state["topics"]
    query = state.get("topics", "")
    if query:
        top_k = 5
        retrieved_docs = faiss_index.similarity_search(query, k=top_k)
        raw_context_local = "\n".join([doc.page_content for doc in retrieved_docs])
    else:
        raw_context_local = ""

    # New Step: Perform web search to get up-to-date information using SerpAPI
    web_summary = get_web_search_summary(query)

    # Merge the local raw context with the web search summary
    combined_context = raw_context_local
    if web_summary:
        combined_context += "\n\nWeb Search Results:\n" + web_summary

    # Step 6: Refine the combined context using the RAG chain
    rag_chain = create_rag_search_chain()
    refined_context = rag_chain.run(
        topics=state.get("topics", ""),
        direction=state.get("direction", ""),
        knowledge_level=state.get("knowledge_level", ""),
        raw_context=combined_context,
    )

    # Step 7: Update state with the refined context and print output
    state["refined_context"] = refined_context.strip()
    print("RAG Search Agent Output:", state["refined_context"])

    # Move to the next node ("rag_script")
    return Command(update=state, goto="rag_script")
