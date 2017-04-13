# LED64 Block Cipher - Fault-Base-Attack & Solution
Fault-based Attacks on LED64 Block Cipher and possible fix for it

[LED64 Block Cipher]( https://sites.google.com/site/ledblockcipher/downloads)
LED64 Design : 
![alt tag](https://sites.google.com/site/ledblockcipher/design/LED64.png?attredirects=0)

Official files from developers can be found in the folder [Official LED](https://github.com/H-Romeo/LED64-Block-Cipher---Fault-Base-Attack-Solution/tree/master/Official%20LED)

LED64 Fault base attack :
[Fault-based Attacks on Cryptographic Hardware](http://ieeexplore.ieee.org/document/6549781/)

![alt tag](https://cloud.githubusercontent.com/assets/27343399/24996308/07312c70-203b-11e7-93b4-c4e2155efe07.png)

## Testing Fault attacks on LED 64 :

In the "Fault-Attack on LED64 - Python" are 3 files, one of them is the LED implementation without the fault attack (led.py), the second one is with the fault attack (led-fault.py) at round 30, and the last file is the attack (attack.py). To test this concept, first generate a ciphertext C with the led.py cipher block, the one without the fault, then generate the C' cipher with fault, and run the attack.py file and paste them there. You will see that the key space is lower than 2^64 due to the fault injected in it.

To run the scripts, no other dependecies except Python 2.7 are required :
```
python2.7 led.py
```

## The Fault :
The attacker aims at determining the value of the secret key K. It is assumed that he can apply a plaintext P of his/her choice to the inputs of a circuit implementing LED-64 and observe the calculated ciphertext C at the outputs of the circuit. Then the calculation is repeated with the same P as the input, and a fault injection is performed. The fault is injected into the state at the beginning of round 30 (i.e., three rounds before the termination of the algorithm)
Since the same P and the same K is used in both cases, the states before fault injection are identical. The fault will propagate to the output, resulting in the faulty ciphertext C' that differs from the correct ciphertext C. The attack requires C and C' to  obtain K by differential cryptanalysis. 

## Solution :
The solution implemented in LED64HR.py dose not fix the fault base attack, but rather makes it harder.
At each SubCell call, where the value `x` is replaced by a value `SBox[x]` according to a lookup table `SBox`, now it shifts the original `SBox` by 1 at each call and it replaces the value `x` with the n'th prime value for the `SBox[x]` value.
Example: if `sbox[state[i][j]] = 5` it replaces that value `state[i][j]` with the 5'th prime number, which is `11`


### Challenge :
Find a way of reducing the keyspace by injecting a fault. The keyspace should be lower than 2^64
