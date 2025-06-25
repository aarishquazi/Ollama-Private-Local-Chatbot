import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class SimpleEncryption:
    def __init__(self, password: str):
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt(self, plaintext: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()

    def decrypt(self, encrypted: str) -> str:
        try:
            raw = base64.b64decode(encrypted)
            iv = raw[:AES.block_size]
            ct = raw[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(ct), AES.block_size).decode()
        except:
            return encrypted