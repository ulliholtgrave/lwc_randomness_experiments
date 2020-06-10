#!/usr/bin/env python
"""
Script to generate test plaintext & keys.
"""

import random
import sys
import getopt
from datetime import datetime

def main(argv):
    """
    Function that includes all data generation steps
    """

    # Provide parameter to generate different types of data.
    mode = ''
    bitlen = 128
    data_type = ''
    try:
        opts, _ = getopt.getopt(argv, "hm:t:b:", ["mode=", "bitlen="])
    except getopt.GetoptError:
        print("""Error: data_generation.py -m <mode> -t <datatype> -b <bitlen>\n
        Args for mode are: 'random', 'low-density', 'high-density' and 'avalanche' \n
        Args for datatype are: 'key' and 'plaintext'. \n
        Args for bitlen: Desired number of bits. Default is 128 bits.""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("data_generation.py -m <mode> -b <bitlen>")
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-t", "--type"):
            data_type = arg
        elif opt in ("-b", "--bitlen"):
            bitlen = int(arg)

    # Check correctness of passed values.
    if mode not in ['random', 'low-density', 'high-density', 'avalanche']:
        print("Unknown parameter '" + mode + "for mode.")
        sys.exit()
    if data_type not in ['key', 'plaintext']:
        print("Unknown parameter '" + data_type + "for type.")
        sys.exit()
    if bitlen <= 1:
        print("The length of the bit sequence is above the required bounds.")
        sys.exit()

    # Select approach of data generation:
    if mode == "random":
        print("Initialize Generator with mode = '" + mode +
              "', datatype = '" + data_type + "' and the size of " + str(bitlen))
        random.seed(a=None, version=2)
        seed = random.getstate()
        save_state(mode, data_type, bitlen, seed)
        data = random.getrandbits(bitlen)
        generate_random_sequence(data, data_type)
    elif mode == "low-density":
        generate_biased_sequence(bitlen, data_type, True)
        save_state(mode, data_type, bitlen, seed=None)
    elif mode == "high-density":
        generate_biased_sequence(bitlen, data_type, False)
        save_state(mode, data_type, bitlen, seed=None)
    else:
        print("No sufficient mode is given. Please fix and re-run the script")
        sys.exit(2)
    #TODO Avalanche


def save_state(mode, data_type, bitlen, seed):
    """
    Function to save current seed and makes an entry to the test log.
    Args:
        seed ([State]): Object provided by the RND saving the current state/seed.
        If the seed is loaded again with setstate() the generator will provide the same outcome.
    """
    log = open("logs/history.txt", "a")
    log_entry = str(datetime.today()) + " - Mode: " + mode + " - DataType: " \
    + data_type + " - Sequence-Length" + str(bitlen) + " - Seed used: " + str(seed) + "\n"
    log.write(log_entry)
    print("Seed Saved")

def generate_random_sequence(data, data_type):
    """
    Generates temporary file with the test data and moves it to the test suite.
    Args:
        data ([int]): Integer generated from the RND.
    """
    if data_type == "key":
        file = open("key.txt", "w", encoding='utf-8')
    elif data_type == "plaintext":
        file = open("plaintext.txt", "w", encoding='utf-8')
    file.write(bin(data)[2:])

def generate_biased_sequence(bitlen, data_type, lowdensity):
    """
    Function to generate biased Data like 0*{0}. Saves it either as key or plaintext.
    Args:
        bitlen (Integeter): Length of the Sequence.
        data_type (String): Differentiates between a key or a plaintext.
        lowdensity (Boolean): True = sequence with high low density (a lot of zeros).
        Otherwise a lot of ones.
    """
    if data_type == "key":
        file = open("key.txt", "w", encoding='utf-8')
    elif data_type == "plaintext":
        file = open("plaintext.txt", "w", encoding='utf-8')
    if lowdensity:
        data = "1"
        data += "".join('0'*(bitlen-1))
    else:
        data = "0"
        data += "".join('1'*(bitlen-1))
    file.write(data)

if __name__ == "__main__":
    main(sys.argv[1:])
