# 🎬 uTubeGist: LangGraph-Powered YouTube Summarizer

**uTubeGist** is an AI agent built using [LangGraph](https://github.com/langchain-ai/langgraph), capable of summarizing YouTube videos, generating timeline-style overviews, and answering questions based on transcript content — all through a modular, state-based workflow.

> 🚀 GPU-ready foundation and clean architecture — ideal for extending into kernel-optimized or high-performance inference tools.

---

## 🔍 Features

- ✂️ **Transcript Chunking**: Automatically fetches and splits YouTube video transcripts.
- 🧠 **LangGraph State Machine**: Each step (fetch → chunk → summarize/QA) is a node in a graph.
- 💬 **Multiple Modes**:
  - Summary
  - Timeline summary
  - Question answering
- 🤖 **LLM-Driven Tasks**: Uses OpenAI's `gpt-3.5-turbo` via LangChain.

---

## 🧱 Architecture

```text
[Fetch Transcript]
        ↓
  [Chunk Transcript]
        ↓
     [Controller] → [Summarize] ───┐
        ↓                         ↓
     [Timeline]                [Q&A]

```
- LangGraph manages transitions based on your selected task mode.

##  🚀 Usage

Follow the prompts:

 - Paste a YouTube video link or ID
 - Choose between summary, timeline, or QA
 - Enjoy the output!

 ##  🧠 Powered By

🗺️ LangGraph
💬 LangChain
🔗 YouTube Transcript API

 ## 🎯 Why It's Impressive

This project showcases:

- Modular graph-based LLM orchestration
- Real-world agentic behavior
- Clean architecture for extending with GPU kernels, TVM, or Triton logic
- Production-ready foundations for UI (Gradio/Streamlit)

  ## 💡 Ideas for Extension

🔥 Add Triton-accelerated summarization kernel
📊 Visual summary dashboards (Gradio)
🎯 Fine-tune controller logic based on video category

