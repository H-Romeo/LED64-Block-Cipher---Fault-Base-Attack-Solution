
MixColMatrix = ((4, 1, 2, 2), (8,6,5,6), (11, 14, 10, 9), (2, 2, 15, 11))
LED = 64
sbox = (12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2)

def FieldMult(a, b):
	ReductionPoly = 0x3
	x = a	
	ret = 0

	for i in range(4):
		if (b>>i)&1:
			ret^=x
		if x&0x8:
			x <<= 1
			x ^= ReductionPoly
		else:
			x <<= 1
	return ret&0xF

def AddKey(state, keybytes,step):
    global LED
    for i in  range(0,4):
        for j in range(0,4):

            state[i][j]^=keybytes[(4*i+j+step*16)%(LED/4)]

def AddConstants(state, r):
    global LED
    RC = (0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F,
		  0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B,
		  0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E,
		  0x1C, 0x38, 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A,
		  0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04)
    
    state[1][0] ^= 0x01
    state[2][0] ^= 0x02
    state[3][0] ^= 0x03
    
    state[0][0] ^= (LED>>4) & 0xF
    state[1][0] ^= (LED>>4) & 0xF
    state[2][0] ^= LED & 0xF
    state[3][0] ^= LED & 0xF

    tmp = (RC[r]>>3) & 0x7
    state[0][1] ^= tmp
    state[2][1] ^= tmp

    tmp =  RC[r] & 0x7
    state[1][1] ^= tmp
    state[3][1] ^= tmp


def SubCell(state):
    global sbox
    for i in range(0,4):
        for j in range(0,4):

            state[i][j]=sbox[state[i][j]]

            


def ShiftRow(state):
    tmp=[0]*4

    for i in range(0,4):
        for j in range(0,4):
            tmp[j]= state[i][j]

        for j in range(0,4):
            state[i][j]=tmp[(j+i)%4]

def MixColumn(state):
    tmp=[0]*4
    for j in range(0,4):
		for i in range(0,4):
			mySum = 0
			for k in range(0,4):
				mySum ^= FieldMult(MixColMatrix[i][k], state[k][j])
                                
			tmp[i] = mySum
		for i in range(4):
			state[i][j] = tmp[i]


def LED_enc(myinput, userkey, ksbits):
        
	state = [[0 for x in range(0,4)] for x in range(0,4)]
        keynibbles = [0]*32
        
	for i in range(0,16):
            if i%2:
                state[i/4][i%4] = myinput[i>>1]&0xF
            else:
                state[i/4][i%4] = myinput[i>>1]>>4&0xF

	for i in range(0,ksbits/4):
            if i%2:
                keynibbles[i] = userkey[i>>1]&0xF
            else:
                keynibbles[i] = (userkey[i>>1]>>4)&0xF

        while len(keynibbles) < 32:
            keynibbles.append(0)

        RN = 48
        if ksbits <= 64:
    	    RN = 32

	AddKey(state, keynibbles, 0)

	for i in range(0,RN/4):
                
		for j in range(0,4):

			AddConstants(state, i*4+j)
			SubCell(state)
			ShiftRow(state)
			MixColumn(state)
                        
                        
		AddKey(state, keynibbles, i+1)

	for i in range(0,8):
	    myinput[i] = ((state[(2*i)/4][(2*i)%4] & 0xF) << 4) | (state[(2*i+1)/4][(2*i+1)%4] & 0xF)

def TestVectors(kbits, p=None, k=None, answer=None):

    c=[0]*8

    for i in range(0,8):
        c[i]=p[i]

    k_str = ""
    for byte in k:
        k_str = k_str + hex(byte).split('x')[1]
    print 'K=', k_str

    p_str = ""
    for byte in p:
        p_str = p_str + hex(byte).split('x')[1]
    print 'P=',p_str

    LED_enc(c,k,kbits)

    c_str = ""
    for byte in c:
        temp = hex(byte).split('x')[1]
        if len(temp) == 1: #add zero padding
            temp = '0'+temp
        c_str = c_str + temp #c_str + hex(byte).split('x')[1]
    print 'C=',c_str

    if answer != None:
        print "checking result matches expected value"
        if c_str == answer:
            print "PASS: ", c_str
        else:
            print "FAIL: ", c_str, "!=", answer, c

        print "--"

def main():

    global LED
    k_vec = []
    p_vec = []
    c_vec = [] 

    print "=============="
    LED = 64
    print 'LED-64: ("theoretically" not vulnerable to fault base attack)'
    #print "using random values in testvectors"
    #TestVectors(64)

    kbits = 64
    p=[0]*8
    k=[0]*16

    print("\nPlaintext: icxcnika - Key: pass1234\n")
    TestVectors(kbits,[0x69,0x63,0x78,0x63,0x6e,0x69,0x6b,0x61],[0x70,0x61,0x73,0x73,0x31,0x32,0x33,0x34])
    #icxcnika   -  pass1234
    

if __name__ == "__main__":
    main()





