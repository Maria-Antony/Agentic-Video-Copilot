from agent_graph import build_graph
from rich import print
from utils import extract_video_id
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    raw_input = input("🎥 Enter YouTube Video ID or URL: ")
    video_id = extract_video_id(raw_input)
    graph = build_graph()
    result = graph.invoke({"video_id": video_id})

    if "summary" in result:
        print("\n📝 [bold cyan]Summary:[/bold cyan]\n")
        print(result["summary"])
    elif "timeline" in result:
        print("\n🕒 [bold magenta]Timeline Summary:[/bold magenta]\n")
        print(result["timeline"])
    elif "qa_answer" in result:
        print("\n🤖 [bold green]Answer:[/bold green]\n")
        print(result["qa_answer"])