from openai import OpenAI

client = OpenAI()

def generate_resources(summary: str, language: str):
    prompt = (
        f"Given the following summary:\n\n{summary[:1000]}\n\n"
        f"Generate a list of 7 useful, real-sounding online resources, books, tutorials or websites "
        f"someone should check to learn more about this topic. "
        f"Write the list in {language}. Each resource should include a short name, and exact URL of the resource "
        f"and 1–2 lines describing what it offers."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()

    # Return as a single text block to display.
    return text
