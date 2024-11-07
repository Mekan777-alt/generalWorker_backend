from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from core.config import settings

key = base64.b64decode(settings.fernet_settings.fernet_key)
IV = base64.b64decode(settings.fernet_settings.fernet_IV)


async def encrypt_phone(phone_number: str) -> str:
    cipher = AES.new(key, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(phone_number.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')


async def decrypt_phone(encrypted_phone: str) -> str:
    encrypted_data = base64.b64decode(encrypted_phone)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')
