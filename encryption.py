"""
Module to provide a basic encryption functionality.
"""

import random
from ctypes import CDLL, POINTER, c_char_p, c_int, c_ulonglong, create_string_buffer, pointer 
from algorithms.py_ascon.ascon import ascon_encrypt

def main():
    """
    Includes all relevant steps for the encryption process.
    """
    with open('key.txt', 'rb') as file:
        key = file.read()
        print("Key: ")
        print(key)
    with open('plaintext.txt', 'rb') as file:
        plaintext = file.read()
        print("Plaintext: ")
        print(plaintext)
    # Generate Nonce
    nonce = generate_nonce(16).encode(encoding='utf-8')
    print("Nonce: ")
    print(nonce)

    # Create empty associated data object
    associated_data = "".encode(encoding='utf-8')

    # Encrypt with python version of Ascon128
    ciphertext = ascon_encrypt(key, nonce, associated_data, plaintext)
    print("Ascon_py Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "ascon128_py_"+str(len(plaintext)))

    # Encrypt with C-Version of Ascon128
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/ascon128.so", 16)
    print("Ascon128 Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "ascon128_c_"+str(len(plaintext)))

    # Encrypt with C-Version of Ascon128a
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/ascon128a.so", 16)
    print("Ascon128a Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "ascon128a_c_"+str(len(plaintext)))

    # Encrypt with Oribatida
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/oribatida.so", 16)
    print("Oribatida Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "oribatida_c_"+str(len(plaintext)))

    # Encrypt with ISAP-A-128
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/isap_a_128.so", 16)
    print("ISAP-A-128 Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "isap_a_c_"+str(len(plaintext)))

    # Encrypt with ISAP-K-128
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/isap_k_128.so", 16)
    print("ISAP-K-128 Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "isap_k_c_"+str(len(plaintext)))

    # Encrypt with SpoC-128
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/spoc_64.so", 16)
    print("SpoC Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "spoc_c_"+str(len(plaintext)))

    # Encrypt with TweGIFT-64_LOTUS-AEAD
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/lotus_64.so", 16)
    print("Lotus_64 Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "lotus_c_"+str(len(plaintext)))

    # Encrypt with TweGIFT-64_LOCUS-AEAD
    ciphertext = encrypt(key, nonce, associated_data, plaintext, "./encryption_interfaces/locus_64.so", 16)
    print("Locus Ciphertext: ")
    print(ciphertext)
    ciphertext = ''.join(format(x, 'b').zfill(8) for x in bytearray(ciphertext))
    save_cipher(ciphertext, "locus_c_"+str(len(plaintext)))

def encrypt(key, nonce, associated_data, plaintext, variant, padding):
    """
    * The CAESAR encrypt interface
    * @param c A pointer to buffer for CT
    * @param clen Ciphertext length in Bytes
    * @param k The secret key
    * @param m A pointer to the PT
    * @param mlen Plaintext length in Bytes
    * @param ad A pointer to associated data
    * @param adlen Length of associated data in Bytes
    * @param npub A pointer to the nonce
    * @param nsec A pointer to secret message number (ignored)
    */
    C Method:
    int crypto_aead_encrypt(unsigned char* c, unsigned long long* clen,
                        const unsigned char* m, unsigned long long mlen,
                        const unsigned char* ad, unsigned long long adlen,
                        const unsigned char* nsec, const unsigned char* npub,
                        const unsigned char* k)
    """
    algorithm = CDLL(variant)
    cbuffer = create_string_buffer(len(plaintext) + padding)
    clen = c_ulonglong()
    algorithm.crypto_aead_encrypt.argtypes = [c_char_p, POINTER(c_ulonglong), c_char_p, c_ulonglong, c_char_p, c_ulonglong, c_char_p, c_char_p, c_char_p]
    algorithm.crypto_aead_encrypt.restype = c_int
    algorithm.crypto_aead_encrypt(cbuffer, pointer(clen), plaintext, len(plaintext), associated_data, len(associated_data), "".encode(encoding='utf-8'), nonce, key)
    return cbuffer.raw


def save_cipher(data, algorithm):
    file = open("ciphertexts/cipher-" + algorithm + ".txt", "w", encoding='utf-8')
    file.write(data)

def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

if __name__ == "__main__":
    main()
