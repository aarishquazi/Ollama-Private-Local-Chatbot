import json
from pathlib import Path
from datetime import datetime

class ConversationStorage:
    def __init__(self, encryption):
        self.encryption = encryption
        self.file = Path("data/conversations.json")
        self.file.parent.mkdir(exist_ok=True)
        self.current_chat = []

    def add(self, role, content):
        self.current_chat.append({"role": role, "content": content, "time": datetime.now().isoformat()})

    def context(self, n=6):
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.current_chat[-n:]])

    def save(self, name):
        data = self.load_all()
        data[name] = [{**m, "content": self.encryption.encrypt(m['content'])} for m in self.current_chat]
        self.file.write_text(json.dumps(data, indent=2))

    def load_all(self):
        return json.loads(self.file.read_text()) if self.file.exists() else {}

    def load(self, name):
        chats = self.load_all()
        self.current_chat = [{**m, "content": self.encryption.decrypt(m['content'])} for m in chats.get(name, [])]

    def clear(self):
        self.current_chat = []