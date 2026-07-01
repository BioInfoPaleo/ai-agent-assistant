import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str

app=FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/hello")
def hello():
    return{"message": "Hello Maryam"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}

@app.post("/summarise")
def summarise(request: SummaryRequest) -> SummaryResponse:
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a translator. Translate the user's text into French"},
            {"role": "user", "content": request.text},
        ],
    )
    summary = completion.choices[0].message.content
    return SummaryResponse(summary=summary)

