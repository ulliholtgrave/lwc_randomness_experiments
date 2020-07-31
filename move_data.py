#!/usr/bin/env python
"""
Provides Functionalities for automating the test harness.
"""

import os
import shutil
import sys
import getopt

def main(argv):
    """
    Function to perform the moving of the test file to the STS.

    Args:
        argv (Strings): Passed Arguments.
    """
    inputfile = ''
    try:
        opts, _ = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    if inputfile != '':
        move_data(inputfile)
    else:
        print("Please provide a valid file that needs to be moved to the STS")

def move_data(ifile):
    """
    Function to move generated testfile to the /data directory of the STS.
    Args:
        file (File): Instance of the generated file with the testdata.
    """
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, ifile)
    destination = os.path.join(dirname, 'sts-2.1.2/data/temp_data.txt')
    shutil.move(file, destination)
    print("Test file moved to Statistical Test Suite")

if __name__ == "__main__":
    main(sys.argv[1:])
    