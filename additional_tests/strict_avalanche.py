import numpy

def test_for_strict_avalanche(plaintext):
    numpy.zeros(len(plaintext), len(plaintext))
    w, h = len(plaintext)
    Matrix = [[0 for x in range(w)] for y in range(h)]

    for x in len(plaintext):
        Matrix[0][x] = plaintext[x]
    print(Matrix)
    for 
