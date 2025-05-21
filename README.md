# RAG
RAG (Retrieval-Augmented Generation)

This Repo has implemented RAG (Retrieval-Augmented Generation) chatbot using Ollama to answer natural language queries from SharePoint-hosted team documents (PDFs); used PyMuPDF for parsing, NLTK for sentence tokenization, and embedding-based semantic search for retrieval. 

#ollama
Ollama can be downloaded from the link here: https://ollama.com/download

After installing, open a terminal and run the following command to download the required models:

```bash
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```
To use ollama in python install the package with the command:
```bash
pip install ollama
```
Run the file catbot.py or AIAbot.py with the following commands:
```bash
python /catbot.py
python /AIAbot.py
```
Inside the RAG folder add in a folder called pdf_folder and add all the pdf files which acts as your external knowledge base. Once all the necessary files are added, the AIAbot will parse the sentences in each file and embedd them. When a query is input, the bot generates a response that has the closest cosine similarity to the query embedding. 

For the catbot to work, a simple text file with lines of facts about cat can be added under the RAG folder.
