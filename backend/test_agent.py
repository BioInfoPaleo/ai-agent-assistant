import os
import json
import pandas as pd
from openai import OpenAI

df = pd.read_csv("bioprocess_data.csv")

def calculate_average(column):
    return float(df[column].mean())

def find_max(column):
    idx = df[column].idxmax()
    return {"run_id": df.loc[idx, "run_id"], "value": float(df[column].max())}

available_tools = {
    "calculate_average": calculate_average,
    "find_max": find_max,
}

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_average",
            "description": "Calculate the average of a numeric column.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {"type": "string", "description": "e.g. 'yield_g_per_l', 'temperature_c', 'ph'"}
                },
                "required": ["column"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_max",
            "description": "Find the row with the highest value in a numeric column, returning its run_id and value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {"type": "string", "description": "e.g. 'yield_g_per_l', 'temperature_c', 'ph'"}
                },
                "required": ["column"],
            },
        },
    },
]

question = "What is the average pH?"
messages = [{"role": "user", "content": question}]

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct:groq",
    messages=messages,
    tools=tools,
)
msg = response.choices[0].message
messages.append(msg)

for call in msg.tool_calls:
    name = call.function.name
    args = json.loads(call.function.arguments)
    result = available_tools[name](**args)
    print(f"  [ran {name}({args}) -> {result}]")
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps(result),
    })

final = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct:groq",
    messages=messages,
)
print("\nAnswer:", final.choices[0].message.content)
