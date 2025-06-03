from langchain.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate.from_template("""
You are a helpful summarizer. Summarize the following transcript:

{text}

Summary:
""")

TIMELINE_PROMPT = PromptTemplate.from_template("""
Create a bulleted summary with timestamps based on the video transcript.
Respond like:
- [00:00] Intro...
- [01:30] Key point...

Text:
{text}

Timeline:
""")