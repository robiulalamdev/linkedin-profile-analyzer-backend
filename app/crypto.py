import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def get_secret() -> bytes:
    secret = os.environ.get("ENCRYPTION_SECRET", "")
    if not secret:
        raise ValueError("ENCRYPTION_SECRET environment variable not set")
    return secret.encode("utf-8")


def _derive_key(secret: bytes, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(secret)


def encrypt(plaintext: str) -> str:
    """Encrypt a string using AES-256-GCM (Node.js-compatible format).

    Format: salt (16) + iv (16) + authTag (16) + ciphertext
    """
    import secrets
    secret = get_secret()
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    key = _derive_key(secret, salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    auth_tag = encryptor.tag

    combined = salt + iv + auth_tag + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def decrypt(ciphertext_b64: str) -> str:
    """Decrypt a base64-encoded ciphertext (Node.js-compatible format).

    Expects format: salt (16) + iv (16) + authTag (16) + ciphertext
    """
    secret = get_secret()
    combined = base64.b64decode(ciphertext_b64)

    salt = combined[:16]
    iv = combined[16:32]
    auth_tag = combined[32:48]
    ciphertext = combined[48:]

    key = _derive_key(secret, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, auth_tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")
