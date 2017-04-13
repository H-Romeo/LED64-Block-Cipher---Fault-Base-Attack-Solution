# LED64-Block-Cipher---Fault-Base-Attack-Solution
Fault-based Attacks on LED64 Block Cipher and possible fix for it

LED64 Block Cipher : https://sites.google.com/site/ledblockcipher/downloads
LED64 Design : 
![alt tag](https://sites.google.com/site/ledblockcipher/design/LED64.png?attredirects=0)

LED64 Fault base attack :
Fault-based Attacks on Cryptographic Hardware :
http://ieeexplore.ieee.org/document/6549781/
![alt tag](https://cloud.githubusercontent.com/assets/27343399/24996308/07312c70-203b-11e7-93b4-c4e2155efe07.png)

##Testing Fault attacks on LED 64 :
In the "Fault-Attack on LED64 - Python" are 3 files, one of them is the LED implementation without the fault attack (led.py), the second one is with the fault attack (led-fault.py) at round 30, and the last file is the attack (attack.py). To test this concept, first generate a ciphertext C with the led.py cipher block, the one without the fault, then generate the C' cipher with fault, and run the attack.py file and paste them there. You will see that the key space is lower than 2^64.
