import streamlit as st
import os
import uuid
from dotenv import load_dotenv

from agents.transcriber import transcribe_youtube, download_audio, transcribe_file
from agents.summarizer import summarize_text
from agents.rag_retriever import generate_resources  # GPT-only version
from agents.exporter import save_as_txt, save_as_pdf
from agents.qa_agent import answer_question
from agents.disk import save_session_to_disk, load_sessions_from_disk

load_dotenv()

st.set_page_config(page_title="Agentic RAG Copilot", page_icon="🎥")

# === Init ===
if "qa_log" not in st.session_state:
    st.session_state.qa_log = []

# Load all sessions from disk
history_list = load_sessions_from_disk()

# === Sidebar ===
with st.sidebar:
    st.title("📑 Session History")

    if history_list:
        history_titles = [
            f"{i+1}. {entry['url_or_file']} | {entry['language']} | QAs: {len(entry['qa_log'])}"
            for i, entry in enumerate(history_list)
        ]

        selected_index = st.selectbox(
            "Pick a session",
            options=list(range(len(history_titles))),
            format_func=lambda i: history_titles[i]
        )

        selected_entry = history_list[selected_index]

        st.markdown(f"**Summary:** {selected_entry['summary'][:150]}...")

        if selected_entry["qa_log"]:
            st.subheader("💬 Q&A Log")
            for qa in selected_entry["qa_log"]:
                st.write(f"**Q:** {qa['q']}")
                st.write(f"**A:** {qa['a']}")
    else:
        st.info("No saved sessions yet.")

# === Main ===
st.title("🎥 Agentic RAG Video Copilot")
st.write("Upload or link a video → get a smart summary, resources & live Q&A.")

option = st.radio("Input Type", ["YouTube URL", "Upload Video"])
url, video_file, target_language = None, None, None

if option == "YouTube URL":
    url = st.text_input("Paste YouTube URL:")
    if url:
        st.video(url)
    target_language = st.selectbox(
        "Target language",
        ["English", "French", "German", "Spanish", "Hindi", "Tamil"]
    )
else:
    video_file = st.file_uploader("Upload your video")
    if video_file:
        st.video(video_file)
    target_language = st.selectbox(
        "Target language",
        ["English", "French", "German", "Spanish", "Hindi", "Tamil"]
    )

length = st.selectbox("Summary Length", ["short", "medium", "long"])
style = st.selectbox("Summary Style", ["paragraph", "notes"])

if st.button("🚀 Process"):
    with st.spinner("⏳ Processing..."):
        transcript = None
        if url:
            transcript = transcribe_youtube(url)
            if not transcript:
                audio_path = download_audio(url)
                transcript = transcribe_file(audio_path)
        elif video_file:
            save_path = os.path.join("uploads", video_file.name)
            with open(save_path, "wb") as f:
                f.write(video_file.read())
            transcript = transcribe_file(save_path)

        summary = summarize_text(transcript, length, style, target_language)
        resources = generate_resources(summary, target_language)

        entry_id = str(uuid.uuid4())
        txt_path = save_as_txt(entry_id, summary, resources)
        pdf_path = save_as_pdf(entry_id, summary, resources)

        # Save current session vars
        st.session_state.url_or_file = url or video_file.name
        st.session_state.summary = summary
        st.session_state.resources = resources
        st.session_state.qa_log = []
        st.session_state.language = target_language

        # Save to disk
        save_session_to_disk({
            "url_or_file": st.session_state.url_or_file,
            "summary": st.session_state.summary,
            "resources": st.session_state.resources,
            "qa_log": st.session_state.qa_log,
            "language": st.session_state.language
        })

    st.subheader("✅ Summary")
    st.write(summary)

    st.subheader("🌐 Suggested Resources")
    st.write(resources)

    with open(txt_path, "rb") as f:
        st.download_button("⬇️ Download TXT", f, file_name="summary.txt")

    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="summary.pdf")

# === Q&A ===
if "summary" in st.session_state and st.session_state.summary:
    st.subheader(f"💬 Ask a question in {st.session_state.language}")
    question = st.text_input("Your question:")

    if st.button("Ask"):
        answer = answer_question(
            st.session_state.summary,
            st.session_state.resources,
            question,
            st.session_state.language
        )
        st.write(f"**A:** {answer}")
        st.session_state.qa_log.append({"q": question, "a": answer})

        # Save updated Q&A to disk (optional)
        save_session_to_disk({
            "url_or_file": st.session_state.url_or_file,
            "summary": st.session_state.summary,
            "resources": st.session_state.resources,
            "qa_log": st.session_state.qa_log,
            "language": st.session_state.language
        })
