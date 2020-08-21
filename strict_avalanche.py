"""
Python Module to apply a SAC test to an algorithm.
"""
import sys
import random
import math
import numpy as np
from bitstring import BitArray
from encryption import encrypt, generate_nonce


def test_for_strict_avalanche():
    """
    Function to apply the SAC test defined in https://eprint.iacr.org/2010/564.pdf.
    """
    with open('key.txt', 'rb') as file:
        key = file.read()
    associated_data = generate_nonce(16).encode(encoding='utf-8')
    sample_size = 32768

    plaintext_bit_size = 64
    plaintext_byte_length = 8
    algorithms = ["ascon128.so", "ascon128a.so", "isap_a_128.so", "isap_k_128.so",
                  "oribatida_128.so", "locus_64.so", "lotus_64.so", "spoc_64.so"]
    print(algorithms)
    for alg in algorithms:
        print(alg)
        if "128" in alg:
            tagsize = 16
        else:
            tagsize = 8
        matrix = np.zeros(
            (plaintext_bit_size, plaintext_bit_size + (tagsize*8)), dtype=int)
        for _ in range(0, sample_size):
            plaintext = random.getrandbits(plaintext_bit_size)
            nonce = generate_nonce(16).encode(encoding='utf-8')
            variant = "encryption_interfaces/" +alg
            original_cipher = encrypt(key, nonce, associated_data, plaintext.to_bytes(
                plaintext_byte_length, sys.byteorder), variant, tagsize)
            for bit_position in range(0, plaintext_bit_size):
                temp_plaintext = BitArray(plaintext.to_bytes(
                    plaintext_byte_length, sys.byteorder))
                temp_plaintext.invert(bit_position)
                nonce = generate_nonce(16).encode(encoding='utf-8')
                cipher = encrypt(key, nonce, associated_data,
                                 temp_plaintext.tobytes(), variant, tagsize)
                cipher_array = BitArray(cipher) ^ BitArray(original_cipher)
                for cipher_position in range(0, plaintext_bit_size + (tagsize*8)):
                    matrix[bit_position][cipher_position] += int(
                        cipher_array.bin[cipher_position])

        flip_probabilty = 0.5
        expected_count = sample_size*flip_probabilty
        with open('sac_results.txt', 'a') as f:
            f.write(variant + "\n")
            for row in range(0, (plaintext_bit_size)):
                for column in range(0, plaintext_bit_size + (tagsize*8)):
                    statistics, pvalue = chisquare([int(matrix[row][column]), int(
                        sample_size - matrix[row][column])], [expected_count, expected_count])
                    f.write(str(pvalue) + "\n")
                    print("Values Stat & P-Value")
                    print(statistics)
                    print(str(pvalue))


def gf(x):
    # Play with these values to adjust the error of the approximation.
    if (x == 0.5):
        return 1.772453850905516027298167483341145182797549456122387128213
    upper_bound = 100.0
    resolution = 1000000.0

    step = upper_bound/resolution

    val = 0
    rolling_sum = 0

    while val <= upper_bound:
        rolling_sum += step * \
            (val**(x-1)*2.7182818284590452353602874713526624977**(-val))
        val += step
    return rolling_sum


def ilgf(s, z):
    val = 0

    for k in range(0, 100):
        val += (((-1)**k)*z**(s+k))/((math.factorial(k))*(s+k))

    return val


def chisquarecdf(x, k):
    return 1-ilgf(k/2, x/2)/gf(k/2)


def chisquare(observed_values, expected_values):
    test_statistic = 0

    for observed, expected in zip(observed_values, expected_values):
        test_statistic += (float(observed)-float(expected))**2/float(expected)

    df = len(observed_values)-1

    return test_statistic, chisquarecdf(test_statistic, df)


if __name__ == "__main__":
    test_for_strict_avalanche()
