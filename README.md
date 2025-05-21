# RAG
RAG (Retrieval-Augmented Generation)

This Repo has implemented RAG (Retrieval-Augmented Generation) chatbot using Ollama to answer natural language queries from SharePoint-hosted team documents (PDFs); used PyMuPDF for parsing, NLTK for sentence tokenization, and embedding-based semantic search for retrieval. 

#ollama
Ollama can be downloaded from the link here: https://ollama.com/download

After installing, open a terminal and run the following command to download the required models:
'''
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
'''
