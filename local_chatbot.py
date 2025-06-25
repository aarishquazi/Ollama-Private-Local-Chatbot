from pathlib import Path
import base64
from encryption import SimpleEncryption
from ollama_manager import OllamaManager
from document_handler import DocumentHandler
from vector_database import VectorDatabase
from conversation_storage import ConversationStorage

class LocalChatbot:
    def __init__(self, password="local_secure_password"):
        self.encryption = SimpleEncryption(password)
        self.ollama = OllamaManager()
        self.docs = DocumentHandler()
        self.vdb = VectorDatabase()
        self.chatlog = ConversationStorage(self.encryption)
        Path("data/files").mkdir(parents=True, exist_ok=True)

    def upload_file(self, file):
        content = file.read()
        enc_content = self.encryption.encrypt(base64.b64encode(content).decode())
        Path(f"data/files/{file.name}").write_text(enc_content)
        chunks = self.docs.process_file(file.name, content)
        self.vdb.add_documents(chunks)
        return len(chunks)

    def answer(self, question: str) -> str:
        docs = self.vdb.search(question)
        if not docs:
            return "No relevant documents found."
        context = "\n\n".join([d['text'] for d in docs])
        prompt = f"Answer this using the context:\n\n{context}\n\nQ: {question}\nA:"
        return self.ollama.get_response(prompt)

    def chat(self, user_input: str) -> str:
        self.chatlog.add("user", user_input)

        if self._should_use_documents(user_input):
            reply = self.answer(user_input)  # Document-based (RAG-style) response
        else:
            prompt = f"Conversation:\n{self.chatlog.context()}\nAssistant:"
            reply = self.ollama.get_response(prompt)  # Conversational response

        self.chatlog.add("assistant", reply)
        return reply


    def _should_use_documents(self, text: str) -> bool:
        """
        Uses the LLM to decide if the input is a question requiring document search.
        """
        system_prompt = "Classify the following message strictly as either 'question' or 'chat':"
        full_prompt = f"{system_prompt}\n\n{text}"
        
        classification = self.ollama.get_response(full_prompt).strip().lower()
        return "question" in classification

