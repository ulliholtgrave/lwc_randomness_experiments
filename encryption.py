"""
Module to provide a basic encryption functionality.
"""
import sys
import random
from ctypes import CDLL, POINTER, c_char_p, c_int, c_ulonglong, create_string_buffer, pointer
from algorithms.py_ascon.ascon import ascon_encrypt


def main(argv):
    """
    Includes all relevant steps for the encryption process.
    """
    associated_data_empty = True
    if len(argv) > 0:
        associated_data_empty = False
    print(argv)

    with open('key.txt', 'rb') as file:
        key = file.read()
    with open('plaintext.txt', 'rb') as file:
        plaintext = file.read()
    # Generate Nonce
    nonce = generate_nonce(16).encode(encoding='utf-8')

    if associated_data_empty:
        # Create empty associated data object
        associated_data = "".encode(encoding='utf-8')
    else:
        # Generate non-empty associated data object
        associated_data = generate_nonce(16).encode(encoding='utf-8')

    # Encrypt with Python version of Ascon128
    ciphertext_py = ascon_encrypt(key, nonce, associated_data, plaintext)
    print("Ascon_py Ciphertext: ")
    ciphertext_py = ''.join(format(x, 'b').zfill(8)
                            for x in bytearray(ciphertext_py))
    save_cipher(ciphertext_py, "ascon128_py_"+str(len(plaintext)))

    # Encrypt with C-Version of Ascon128
    ciphertext = encrypt(key, nonce, associated_data,
                         plaintext, "./encryption_interfaces/ascon128.so", 16)
    print("Ascon128 Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "ascon128_c_"+str(len(plaintext)))

    # Check for Integrity
    print("Python and C cipher are identical: " +
          str(ciphertext == ciphertext_py))

    # Encrypt with C-Version of Ascon128a
    ciphertext = encrypt(key, nonce, associated_data,
                         plaintext, "./encryption_interfaces/ascon128a.so", 16)
    print("Ascon128a Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "ascon128a_c_2"+str(len(plaintext)))

    # Encrypt with Oribatida 128
    ciphertext = encrypt(key, nonce, associated_data, plaintext,
                         "./encryption_interfaces/oribatida_128.so", 16)
    print("Oribatida Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "oribatida_c_"+str(len(plaintext)))

    # Encrypt with ISAP-A-128
    ciphertext = encrypt(key, nonce, associated_data, plaintext,
                         "./encryption_interfaces/isap_a_128.so", 16)
    print("ISAP-A-128 Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "isap_a_c_"+str(len(plaintext)))

    # Encrypt with ISAP-K-128
    ciphertext = encrypt(key, nonce, associated_data, plaintext,
                         "./encryption_interfaces/isap_k_128.so", 16)
    print("ISAP-K-128 Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "isap_k_c_"+str(len(plaintext)))

    # Encrypt with SpoC-64
    ciphertext = encrypt(key, nonce, associated_data,
                         plaintext, "./encryption_interfaces/spoc_64.so", 8)
    print("SpoC Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "spoc_c_"+str(len(plaintext)))

    # Encrypt with TweGIFT-64_LOTUS-AEAD
    ciphertext = encrypt(key, nonce, associated_data,
                         plaintext, "./encryption_interfaces/lotus_64.so", 8)
    print("Lotus_64 Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "lotus_c_"+str(len(plaintext)))

    # Encrypt with TweGIFT-64_LOCUS-AEAD
    ciphertext = encrypt(key, nonce, associated_data,
                         plaintext, "./encryption_interfaces/locus_64.so", 8)
    print("Locus Ciphertext: ")
    ciphertext = ''.join(format(x, 'b').zfill(8)
                         for x in bytearray(ciphertext))
    save_cipher(ciphertext, "locus_c_"+str(len(plaintext)))


def encrypt(key, nonce, associated_data, plaintext, variant, padding):
    """
    Args:
        key (Byte): 8 Byte key.
        nonce (Byte): 8 Byte nonce.
        associated_data (Byte): Either 128 Bit Integer or empty.
        plaintext (Byte): Plaintext in Byte.
        variant (String): Path to shared Object.
        padding (Integer): Length of the tag.
    Returns:
        [Bytes]: The encrypted bytes object.
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
    algorithm.crypto_aead_encrypt.argtypes = [c_char_p, POINTER(
        c_ulonglong), c_char_p, c_ulonglong, c_char_p, c_ulonglong, c_char_p, c_char_p, c_char_p]
    algorithm.crypto_aead_encrypt.restype = c_int
    algorithm.crypto_aead_encrypt(cbuffer, pointer(clen), plaintext, len(
        plaintext), associated_data, len(associated_data), "".encode(encoding='utf-8'), nonce, key)
    return cbuffer.raw


def save_cipher(data, algorithm):
    """
    Saves the to the corresponding file.
    BE AWARE that this call APPENDS the cipher to the file.

    Args:
        data (String): The ciphertext.
        algorithm (String): Name of the examined algorithm.
    """
    file = open("ciphertexts/cipher-" + algorithm +
                ".txt", "a", encoding='utf-8')
    file.write(data)


def generate_nonce(length=8):
    """
    Generate the bit representation to a random integer. 

    Args:
        length (int, optional): Desired number of bits. Defaults to 8.

    Returns:
        [String]: Binary representation as a String.
    """
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


if __name__ == "__main__":
    main(sys.argv[1:])
