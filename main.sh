#!/bin/bash

# This Script includes all preparation steps necessary for the experiment.

# Data generation
echo "Starting plaintext Generation"

# Real-world random key empty associated data
python3 data_generation.py -m real-world -t plaintext -b 10000000
python3 data_generation.py -m random -t key -b 16
python3 encryption.py

# Real-world random key set associated data
python3 encryption.py True

# Real-world high-density key empty associated data
python3 data_generation.py -m high-density -t key -b 16
python3 encryption.py

# Real-world high-density key set associated data
python3 encryption.py True

# Real-world low-density key empty associated data
python3 data_generation.py -m low-density -t key -b 16
python3 encryption.py

# Real-world low-density key set associated data
python3 encryption.py True

# ----------------------------------

# Random Plaintext random key empty associated data
python3 data_generation.py -m random -t plaintext -b 10000000
python3 data_generation.py -m random -t key -b 16
python3 encryption.py

# Random Plaintext random key set associated data
python3 encryption.py True

# Random Plaintext high-density key empty associated data
python3 data_generation.py -m high-density -t key -b 16
python3 encryption.py

# Random Plaintext high-density key set associated data
python3 encryption.py True

# Random Plaintext low-density key empty associated data
python3 data_generation.py -m low-density -t key -b 16
python3 encryption.py

# Random Plaintext low-density key set associated data
python3 encryption.py True

# ----------------------------------

# High-density Plaintext random key empty associated data
python3 data_generation.py -m high-density -t plaintext -b 10000000
python3 data_generation.py -m random -t key -b 16
python3 encryption.py

# High-density Plaintext random key set associated data
python3 encryption.py True

# High-density Plaintext high-density key empty associated data
python3 data_generation.py -m high-density -t key -b 16
python3 encryption.py

# High-density Plaintext high-density key set associated data
python3 encryption.py True

# High-density Plaintext low-density key empty associated data
python3 data_generation.py -m low-density -t key -b 16
python3 encryption.py

# Random Plaintext low-density key set associated data
python3 encryption.py True

# ----------------------------------

# High-density Plaintext random key empty associated data
python3 data_generation.py -m low-density -t plaintext -b 10000000
python3 data_generation.py -m random -t key -b 16
python3 encryption.py

# High-density Plaintext random key set associated data
python3 encryption.py True

# High-density Plaintext high-density key empty associated data
python3 data_generation.py -m high-density -t key -b 16
python3 encryption.py

# High-density Plaintext high-density key set associated data
python3 encryption.py True

# High-density Plaintext low-density key empty associated data
python3 data_generation.py -m low-density -t key -b 16
python3 encryption.py

# Random Plaintext low-density key set associated data
python3 encryption.py True



# Move Cipher to STS

#python3 move_data.py -i cipher.txt



