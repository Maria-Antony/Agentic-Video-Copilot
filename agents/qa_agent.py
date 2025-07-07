from openai import OpenAI

client = OpenAI()

def answer_question(summary, resources, question):
    context = f"{summary}\n\nResources:\n"
    for r in resources:
        context += f"{r['title']}: {r['snippet']}\n"
    prompt = f"Answer this question using the video context:\n\nQ: {question}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
