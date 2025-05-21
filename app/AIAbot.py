import os
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
import ollama
from pathlib import Path

nltk.download('punkt')

dataset = []

pdf_folder = Path(r'C:\Users\sadha\Documents\Projects\RAG\pdf_folder')

for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        filepath = os.path.join(pdf_folder, filename)
        doc = fitz.open(filepath)
        full_text = ''
        for page in doc:
            full_text += page.get_text()
        sentences = sent_tokenize(full_text)
        dataset.extend(sentences)

print(f'Loaded {len(dataset)} sentences from PDF documents')

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]
VECTOR_DB = []

def add_chunk_to_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  VECTOR_DB.append((chunk, embedding))

def cosine_similarity(a, b):
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
  query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
  # temporary list to store (chunk, similarity) pairs
  similarities = []
  for chunk, embedding in VECTOR_DB:
    similarity = cosine_similarity(query_embedding, embedding)
    similarities.append((chunk, similarity))
  # sort by similarity in descending order, because higher similarity means more relevant chunks
  similarities.sort(key=lambda x: x[1], reverse=True)
  # finally, return the top N most relevant chunks
  return similarities[:top_n]

for i, chunk in enumerate(dataset):
  add_chunk_to_database(chunk)
  print(f'Added chunk {i+1}/{len(dataset)} to the database')

while True:
  input_query = input('\nAsk me a question (or type "exit" to quit): ').strip()
  if input_query.lower() in {'exit', ''}:
      print("Goodbye! See you soon...")
      break

  retrieved_knowledge = retrieve(input_query)

  print('\nRetrieved knowledge:')
  for chunk, similarity in retrieved_knowledge:
    print(f' - (similarity: {similarity:.2f}) {chunk}')

  context_chunks = '\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])
  instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{context_chunks}'''

  stream = ollama.chat(
    model=LANGUAGE_MODEL,
    messages=[
      {'role': 'system', 'content': instruction_prompt},
      {'role': 'user', 'content': input_query},
    ],
    stream=True,
  )

  print('\nChatbot response:')
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
