"""
Module to provide a basic encryption functionality.
"""

import random
from algorithms.py_ascon.ascon import ascon_encrypt


def main():
    with open('key.txt', 'r', encoding='utf-8') as file:
        key = file.read().encode(encoding='utf-8')
        print(type(key))
        print(len(key))
        print(key)
    with open('plaintext.txt', 'r', encoding='utf-8') as file:
        data = file.read().encode(encoding='utf-8')
        print(data)
    nonce = generate_nonce(16).encode(encoding='utf-8')
    print(nonce)
    print(len(nonce))
    associated_data = generate_nonce(10).encode(encoding='utf-8')
    print(associated_data)

    ciphertext = ascon_encrypt(key, nonce, associated_data, data)
    print(ciphertext)
    save_cipher(str(ciphertext))

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def save_cipher(data):
    file = open("cipher.txt", "w", encoding='utf-8')
    file.write(data)

if __name__ == "__main__":
    main()
