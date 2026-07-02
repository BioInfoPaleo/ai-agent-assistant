import os
import chromadb
from openai import OpenAI

# --- Set up the LLM client  ---
llm = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# --- Set up Chroma and load the docs ) ---
chroma = chromadb.Client()
collection = chroma.create_collection(name="csl_docs")

documents = {
    "overview": """CSL is a global biotechnology company dedicated to developing and delivering innovative medicines that help people with serious and rare diseases. Founded in Australia over a century ago, it operates across more than 100 countries. CSL Behring develops plasma-derived therapies and recombinant treatments. Seqirus is one of the world's largest influenza vaccine providers. CSL Vifor focuses on therapies for iron deficiency, kidney disease and nephrology. Its mission is to save lives and improve quality of life for people with serious diseases.""",
    "sustainability": """CSL views sustainability as integral to its long-term strategy. Environmental priorities include reducing greenhouse gas emissions, improving energy efficiency, responsible water management, reducing waste and increasing recycling, and investing in sustainable manufacturing. Socially, CSL expands access to medicines, promotes diversity and inclusion, and supports communities. Governance covers ethics, risk management, regulatory compliance, responsible sourcing, and data privacy.""",
    "innovation": """Innovation is fundamental to CSL. It invests billions of dollars in research and development to discover novel therapies, improve treatments, develop advanced biologics, and expand options for rare diseases. CSL collaborates with universities, research institutes, biotechnology companies and healthcare providers. Innovation extends into manufacturing through automation, digital systems and quality control, always guided by patient needs.""",
}

for doc_id, text in documents.items():
    collection.add(documents=[text], ids=[doc_id], metadatas=[{"source": doc_id}])

# --- The RAG function ---
def ask(question):
    # 1. RETRIEVE: find the most relevant chunks
    results = collection.query(query_texts=[question], n_results=2)
    retrieved_chunks = results["documents"][0]

    # 2. BUILD CONTEXT: join the chunks into one string
    context = "\n\n".join(retrieved_chunks)

    # 3. GENERATE: ask Llama, giving it the context
    completion = llm.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer the user's question using ONLY the provided context. If the answer isn't in the context, say you don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return completion.choices[0].message.content

# --- Try it ---
question = "How does CSL protect the environment?"
answer = ask(question)
print(f"Q: {question}\n")
print(f"A: {answer}")
