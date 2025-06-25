# 🧠 Local Document Chatbot

A private, offline chatbot that can:
- Chat with you conversationally
- Answer questions based on your uploaded documents (RAG-style)
- Use open-source LLMs via [Ollama](https://ollama.com)
- Run entirely on your local machine — no API keys or internet required

---

## 🚀 Features

- 💬 **Conversational Mode** – Natural, context-aware chat
- 📄 **Document Question Answering** – Asks and answers questions from uploaded PDFs or files
- 🔐 **Offline & Private** – Powered by local models using Ollama, no data sent outside
- ⚡ **Streamlit UI** – Simple and fast web interface
- 🧠 **Intent Detection** – Smart routing of questions vs. chat using LLM-based classification

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io) – frontend interface
- [Ollama](https://ollama.com) – local LLM runtime (e.g., `llama3`, `mistral`)
- [ChromaDB](https://www.trychroma.com) – local vector store
- [Python](https://www.python.org/) – backend logic
- Optional: `LangChain`, `PyPDF`, `FAISS`, or others if customized

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/local-document-chatbot.git
   cd local-document-chatbot

2. **Create a virtual environment**

```bash
    python -m venv env
    source env/bin/activat
    
3. **Install dependencies**

    ```bash
    pip install -r requirements.txt

4. **Install and run Ollama**

    - Download Ollama

    - tart a model (e.g., llama3)

    ```bash
    ollama run llama3
    Run the app
    streamlit run main.py

## 📌 Notes

- Make sure Ollama is running before starting the app.

- Document-based Q&A is only triggered when your input is a question (classified by the model).
