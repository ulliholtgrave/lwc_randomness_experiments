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
    bytelen = 128
    data_type = ''
    try:
        opts, _ = getopt.getopt(argv, "hm:t:b:", ["mode=", "bytelen="])
    except getopt.GetoptError:
        print("""Error: data_generation.py -m <mode> -t <datatype> -b <bytelen>\n
        Args for mode are: 'random', 'low-density', 'high-density' and 'real-world' \n
        Args for datatype are: 'key' and 'plaintext'. \n
        Args for bytelen: Desired number of bits. Default is 128 bits.""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("data_generation.py -m <mode> -b <bytelen>")
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-t", "--type"):
            data_type = arg
        elif opt in ("-b", "--bytelen"):
            bytelen = int(arg)

    # Check correctness of passed values.
    if mode not in ['random', 'low-density', 'high-density', 'real-world']:
        print("Unknown parameter '" + mode + "for mode.")
        sys.exit()
    if data_type not in ['key', 'plaintext']:
        print("Unknown parameter '" + data_type + "for type.")
        sys.exit()
    if bytelen <= 1:
        print("The length of the bit sequence is above the required bounds.")
        sys.exit()

    # Select approach of data generation:
    if mode == "random":
        print("Initialize Generator with mode = '" + mode +
              "', datatype = '" + data_type + "' and the size of " + str(bytelen))
        random.seed(a=None, version=2)
        seed = random.getstate()
        save_state(mode, data_type, bytelen, seed)
        data = random.getrandbits(bytelen*8)
        generate_random_sequence(data, data_type, bytelen)
    elif mode == "low-density":
        generate_biased_sequence(bytelen, data_type, True)
        save_state(mode, data_type, bytelen, seed=None)
    elif mode == "high-density":
        generate_biased_sequence(bytelen, data_type, False)
        save_state(mode, data_type, bytelen, seed=None)
    elif mode == "real-world":
        generate_real_plaintext(bytelen)
    else:
        print("No existing mode is given. Please fix and re-run the script")
        sys.exit(2)


def save_state(mode, data_type, bytelen, seed):
    """
    Function to save current seed and makes an entry to the test log.
    Args:
        seed ([State]): Object provided by the RND saving the current state/seed.
        If the seed is loaded again with setstate() the generator will provide the same outcome.
    """
    log = open("logs/history.txt", "a")
    log_entry = str(datetime.today()) + " - Mode: " + mode + " - DataType: " \
        + data_type + " - Sequence-Length" + \
        str(bytelen) + " - Seed used: " + str(seed) + "\n"
    log.write(log_entry)
    print("Seed Saved")


def generate_random_sequence(data, data_type, bytelen):
    """
    Generates temporary file with the test data.
    Args:
        data ([int]): Integer generated from the RND.
    """
    if data_type == "key":
        file = open("key.txt", "wb")
    elif data_type == "plaintext":
        file = open("plaintext.txt", "wb")
    file.write(data.to_bytes(bytelen, sys.byteorder))  # ENDIANESS


def generate_biased_sequence(bytelen, data_type, lowdensity):
    """
    Function to generate biased Data like 0*{0}. Saves it either as key or plaintext.
    Args:
        bytelen (Integer): Length of the Sequence.
        data_type (String): Differentiates between a key or a plaintext.
        lowdensity (Boolean): True = sequence with high low density (a lot of zeros).
        Otherwise a lot of ones.
    """
    if data_type == "key":
        file = open("key.txt", "wb")
    elif data_type == "plaintext":
        file = open("plaintext.txt", "wb")
    if lowdensity:
        data = 128
        file.write(data.to_bytes(bytelen, sys.byteorder))
    else:
        data = 127
        file.write(data.to_bytes(1, sys.byteorder))
        for _ in range(0, bytelen-1):
            data = 255
            file.write(data.to_bytes(1, sys.byteorder))


def generate_real_plaintext(bytelen):
    """
    Function to provide "real-world" data by using the CrackStation dictionary (crackstation.txt).
    As the dictionary consists of different kinds of data (real password leaks, XML/HTML text, plaintext) a random sample of the file is used.
    Args:
        bytelen (Integer): Defines the required length of bytes of the data.
    """
    try:
        for _ in range(0, 10):
            in_file = open("crackstation.txt", "rb")
            offset = random.randrange(1000000000)
            in_file.seek(offset)
            data = in_file.read(int(bytelen / 10))
            out_file = open("plaintext.txt", "wb")
            out_file.write(data)
    except OSError:
        print("It seems like the crackstation.txt isn't existing so far. Please check if you have to decompress the crackstation.txt.gz file first.")


if __name__ == "__main__":
    main(sys.argv[1:])
