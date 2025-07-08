import streamlit as st
import os
import uuid
from dotenv import load_dotenv

from graph import compiled_graph  
from agents.exporter import save_as_txt, save_as_pdf
from agents.disk import save_session_to_disk, load_sessions_from_disk

load_dotenv()

st.set_page_config(page_title="Agentic Video Copilot", page_icon="🎥")

# === Init session ===
if "qa_log" not in st.session_state:
    st.session_state.qa_log = []

history_list = load_sessions_from_disk()


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

# Main 
st.title("🎥 Agentic Video Copilot")
st.write("Upload or link a video → get a summary, learning resources & live Q&A.")

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

# Process button: runs full graph 
if st.button("🚀 Process"):
    with st.spinner("⏳ Processing"):
        file_path = None
        if video_file:
            save_path = os.path.join("uploads", video_file.name)
            with open(save_path, "wb") as f:
                f.write(video_file.read())
            file_path = save_path

        input_state = {
            "url": url,
            "file_path": file_path,
            "transcript": None,
            "summary": None,
            "resources": None,
            "question": None,  # no question yet
            "last_answer": None,
            "qa_log": [],
            "length": length,
            "style": style,
            "language": target_language
        }

        output = compiled_graph.invoke(input_state)

        summary = output["summary"]
        resources = output["resources"]

        entry_id = str(uuid.uuid4())
        txt_path = save_as_txt(entry_id, summary, resources)
        pdf_path = save_as_pdf(entry_id, summary, resources)

        # Store in session_state for Q&A
        st.session_state.url_or_file = url or video_file.name
        st.session_state.summary = summary
        st.session_state.resources = resources
        st.session_state.qa_log = []
        st.session_state.language = target_language

        # Save to disk
        save_session_to_disk({
            "url_or_file": st.session_state.url_or_file,
            "summary": summary,
            "resources": resources,
            "qa_log": [],
            "language": target_language
        })

    st.subheader("✅ Summary")
    st.write(summary)

    st.subheader("🌐 Suggested Resources")
    st.write(resources)

    with open(txt_path, "rb") as f:
        st.download_button("⬇️ Download TXT", f, file_name="summary.txt")

    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="summary.pdf")

# Q&A Node: re-invoke graph with question 
if "summary" in st.session_state and st.session_state.summary:
    st.subheader(f"💬 Ask a question in {st.session_state.language}")
    question = st.text_input("Your question:")

    if st.button("Ask"):
        q_state = {
            "url": None,
            "file_path": None,
            "transcript": None,
            "summary": st.session_state.summary,
            "resources": st.session_state.resources,
            "question": question,  # 👈 user question
            "last_answer": None,
            "qa_log": st.session_state.qa_log,
            "length": "",
            "style": "",
            "language": st.session_state.language
        }

        output = compiled_graph.invoke(q_state)
        answer = output["last_answer"]

        st.write(f"**A:** {answer}")

        st.session_state.qa_log.append({"q": question, "a": answer})

        save_session_to_disk({
            "url_or_file": st.session_state.url_or_file,
            "summary": st.session_state.summary,
            "resources": st.session_state.resources,
            "qa_log": st.session_state.qa_log,
            "language": st.session_state.language
        })
