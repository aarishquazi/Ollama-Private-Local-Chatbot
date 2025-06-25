from pathlib import Path
from typing import List, Dict
from io import BytesIO
import PyPDF2
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentHandler:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def read_pdf(self, content: bytes):
        reader = PyPDF2.PdfReader(BytesIO(content))
        return "".join([p.extract_text() for p in reader.pages])

    def read_docx(self, content: bytes):
        doc = docx.Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])

    def read_txt(self, content: bytes):
        return content.decode('utf-8')

    def process_file(self, filename: str, content: bytes) -> List[Dict]:
        ext = Path(filename).suffix.lower()
        if ext == ".pdf": text = self.read_pdf(content)
        elif ext == ".docx": text = self.read_docx(content)
        elif ext in [".txt", ".md"]: text = self.read_txt(content)
        else: raise ValueError("Unsupported file type")

        chunks = self.splitter.split_text(text)
        return [{"id": f"{filename}_{i}", "text": ch, "source": filename, "chunk": i} for i, ch in enumerate(chunks)]