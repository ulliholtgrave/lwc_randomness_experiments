#!/bin/bash

# This Script includes all preparation steps necessary for the experiment.


# Data generation
echo "Starting plaintext Generation"


# TODO Loop for larger number of sequences
python3 data_generation.py -m random -t plaintext -b 128


echo "Starting key Generation"
python3 data_generation.py -m low-density -t key -b 16

# Encryption

python3 encryption.py

# Move to STS

# python3 move_data.py -i cipher.txt



