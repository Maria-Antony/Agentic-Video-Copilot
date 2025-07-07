from openai import OpenAI

client = OpenAI()

def summarize_text(transcript: str, length: str, style: str, language:str) -> str:
    prompt = (
        f"Summarize this video transcript in a {length} length and {style} format and in {language}:\n\n"
        f"{transcript[:2000]}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
