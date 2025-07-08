from langgraph.graph import StateGraph, START, END
from agents.transcriber import transcribe_youtube, download_audio, transcribe_file
from agents.summarizer import summarize_text
from agents.rag_retriever import generate_resources
from agents.qa_agent import answer_question
from typing_extensions import TypedDict
import os

# --- State ---
class VideoGraphState(TypedDict):
    url: str | None
    file_path: str | None
    transcript: str | None
    summary: str | None
    resources: str | None
    question: str | None
    last_answer: str | None
    qa_log: list[dict]
    length: str
    style: str
    language: str

# --- Nodes ---
def transcriber_node(state: VideoGraphState) -> VideoGraphState:
    url = state.get("url")
    file_path = state.get("file_path")
    transcript = ""

    if url:
        transcript = transcribe_youtube(url)
        if not transcript:
            audio_path = download_audio(url)
            transcript = transcribe_file(audio_path)
    elif file_path:
        transcript = transcribe_file(file_path)

    state["transcript"] = transcript
    return state

def summarizer_node(state: VideoGraphState) -> VideoGraphState:
    summary = summarize_text(state["transcript"], state["length"], state["style"], state["language"])
    state["summary"] = summary
    return state

def rag_node(state: VideoGraphState) -> VideoGraphState:
    resources = generate_resources(state["summary"], state["language"])
    state["resources"] = resources
    return state

def qa_node(state: VideoGraphState) -> VideoGraphState:
    question = state.get("question")
    if not question:
        return state

    answer = answer_question(
        state["summary"],
        state["resources"],
        question,
        state["language"]
    )
    if "qa_log" not in state:
        state["qa_log"] = []
    state["qa_log"].append({"q": question, "a": answer})
    state["last_answer"] = answer
    return state

# --- Graph ---
workflow = StateGraph(VideoGraphState)

workflow.add_node("Transcriber", transcriber_node)
workflow.add_node("Summarizer", summarizer_node)
workflow.add_node("RAG", rag_node)
workflow.add_node("Q&A", qa_node)

workflow.set_entry_point("Transcriber")
workflow.add_edge("Transcriber", "Summarizer")
workflow.add_edge("Summarizer", "RAG")
workflow.add_edge("RAG", "Q&A")
workflow.add_edge("Q&A", END)

compiled_graph = workflow.compile()
