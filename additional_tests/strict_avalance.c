#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double SAC8_test (unsigned long (*rng)()){const unsigned long m = 10000;
    unsigned int n,i,j; 
    unsigned long xor8, xor32, alea[m];
    int ea8count[8]; 
    int hamming8 = 0;
    float expected = 0.0, suma = 0.0; 
    float chi8 = 0.0;
    for (i=0;i<9;i++) ea8count[i]=0;
    for (i=0;i<m; ++i) alea[i] = rng();
    for (i=0;i<m;++i){hamming8 = 0;
    xor32 = alea[i] ^ alea[i+ 1]; 
    xor8 = xor32;
    for(j=0;j< 32;j++){
        if (xor8&1) hamming8++; 
        xor8 = xor8 & 1;
        if ((j%8) == 7){
            ea8count[hamming8]++; 
            hamming8 = 0;}
        }
    }
    chi8 = 0.0;
    for (i=0;i<9;i++){
        expected = (4*m) * prob(8,i);
        if (expected > 5.0)suma = (expected-ea8count[i])*(expected-ea8count[i])/expected;
        else suma = 0;
        chi8 = chi8+suma;
        }
    printf("This adds up to a value %3.9f of chi-square-8 \n",chi8);
}