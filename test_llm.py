import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that summarises text concisely."},
        {"role": "user", "content": "Photosynthesis is the process by which green plants use sunlight to turn carbon dioxide and water into glucose and oxygen."},
    ],
)

print(completion.choices[0].message.content)