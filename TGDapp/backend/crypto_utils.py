import time
from ecdsa import SigningKey, SECP256k1

def generate_signature(private_key_hex):
    timestamp = str(int(time.time()))
    sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    signature = sk.sign(timestamp.encode())
    return timestamp, signature.hex()