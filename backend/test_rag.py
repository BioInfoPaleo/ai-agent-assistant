import chromadb

client = chromadb.Client()
collection = client.create_collection(name="csl_docs")

# Your three documents, as text
documents = {
    "overview": """CSL is a global biotechnology company dedicated to developing and delivering innovative medicines that help people with serious and rare diseases. Founded in Australia over a century ago, it operates across more than 100 countries. CSL Behring develops plasma-derived therapies and recombinant treatments for rare and serious conditions including immunology, hematology, respiratory, cardiovascular and transplant medicine. Seqirus is one of the world's largest influenza vaccine providers, supplying seasonal and pandemic influenza vaccines globally. CSL Vifor focuses on therapies for iron deficiency, kidney disease and nephrology. The company invests significantly in research and development, operates a worldwide network of manufacturing facilities, plasma collection centres and research laboratories, and maintains rigorous quality standards. Its mission is to save lives and improve quality of life for people with serious diseases.""",

    "sustainability": """CSL views sustainability as an integral part of its long-term strategy, aiming to create value for patients, employees, communities and shareholders while protecting the environment. Key environmental priorities include reducing greenhouse gas emissions, improving energy efficiency across operations, responsible water management, reducing waste and increasing recycling, and investing in more sustainable manufacturing processes. Socially, CSL expands access to lifesaving medicines, promotes diversity, equity and inclusion, invests in employee wellbeing, and supports local communities through charitable partnerships and educational initiatives. Strong governance covers corporate ethics, risk management, regulatory compliance, responsible sourcing, and data privacy and cybersecurity. The company aligns its initiatives with internationally recognised sustainability frameworks and reports progress on its commitments.""",

    "innovation": """Innovation is fundamental to CSL's ability to develop new therapies for unmet medical needs. CSL invests billions of dollars in research and development to discover novel therapies, improve existing treatments, develop advanced biologic medicines, and expand options for rare diseases. Research spans immunology, hematology, cardiovascular disease, respiratory medicine and nephrology. The company collaborates with universities, medical research institutes, biotechnology companies, healthcare providers and international scientific organisations to accelerate research and bring discoveries into clinical development. Innovation extends into manufacturing through modern production facilities, automation technologies, digital manufacturing systems, quality control processes and supply chain improvements. Every stage of innovation is guided by patient needs, aiming for therapies that are safer, more effective and more accessible.""",
}

# Add each document to Chroma
for doc_id, text in documents.items():
    collection.add(
        documents=[text],
        ids=[doc_id],
        metadatas=[{"source": doc_id}],
    )

print(f"Loaded {len(documents)} documents.")

# Ask a question
results = collection.query(
    query_texts=["What vaccines does CSL make?"],
    n_results=2,
)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"\n--- From: {meta['source']} ---")
    print(doc)