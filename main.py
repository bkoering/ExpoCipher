import random

g=2
# --------------------------------------


def primeGenerator():  # generates a random 31 bit number

    prime = "1"

    for i in range(29):
        prime += str(random.randint(0, 1))

    prime += "1"
    prime = int(prime,2)

    return prime

# --------------------------------------

def millerRabin(n):

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1

    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(64):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break

        else:
            return False

    return True

# --------------------------------------


def keyGenerator():
    p = 10

    while not millerRabin(p):
        q = 10

        while ((q % 12) != 5) or (not millerRabin(q)):
            q = primeGenerator()

        p = (2 * q) + 1

    d = random.randint(1, p)
    e2 = pow(g, d, p)

    pubKey= str(p) + " " + str(g) + " " + str(e2)
    priKey= str(p) + " " + str(g) + " " + str(d)
    open("prikey.txt", 'w').write(priKey)
    open("pubkey.txt", 'w').write(pubKey)

    print ("public key=", pubKey, "            private key=", priKey)

# --------------------------------------

def encryption():
    pubKey = open("pubkey.txt").read().split()
    plainText = open("ptext.txt").read()

    print ("contents of file pText= ", plainText)


    p= int(pubKey[0])
    g= int(pubKey[1])
    e2= int(pubKey[2])

    blockCount = len(plainText)//4
    if (len(plainText) % 4) != 0:
        blockCount += 1
    C= ""

    for i in range(blockCount):
        k = random.randint(0, p)

        block = plainText[4*i:4*i + 4]

        # fill with whitespace where needed
        block += ' '*(4 - len(block))

        m= ord(block[0]) + 256*(ord(block[1]) + 256*(ord(block[2]) + 256*ord(block[3])))

        c1= bin(pow(g, k, p))[2:]
        c2= pow(e2, k, p) * m
        c2= bin(c2 % p)[2:]

        #pad w/ 0s then concatenate on C
        C += '0'*(32-len(c1)) + c1 + '0'*(32 - len(c2)) + c2

    encryptedText = str(int(C, 2))

    open("ctext.txt", 'w').write(encryptedText)
    print ("encrypted text = ", encryptedText)


# --------------------------------------
def decryption():
    privateKey = open("prikey.txt").read().split()
    C= bin(int(open("ctext.txt").read()))[2:]

    p= int(privateKey[0])
    g= int(privateKey[1])
    d= int(privateKey[2])


    pad= 32 - (len(C) % 32)
    pad= pad%32

    encryptedBinaryString= '0'*pad + C
    blockCount= len(encryptedBinaryString) // 64
    decryptedText = ""

    for i in range(blockCount):
        C= encryptedBinaryString[64*i:64*i + 64]

        #m = ( (c1^(p-1-d) mod p)*c2 ) mod p
        mInt= (pow(int(C[0:32], 2), p-1-d, p) * int(C[32:], 2))
        mInt= mInt%p


        mString= chr(mInt & 0xFF) + chr((mInt & 0xFF00) >> 8) + chr((mInt & 0xFF0000) >> 16) + chr((mInt & 0xFF000000) >> 24)
        decryptedText += mString

    open("dtext.txt", 'w').write(decryptedText)
    print ("decrypted text = ", decryptedText)


# --------------------------------------


def main():
    while 1:
        print("Please enter one of the following")
        print("k - key generation")
        print("e - encrypt text")
        print("d - decrypt text")
        print("q - quit")
        command = input("\n").lower()

        if command == 'q':
            return

        elif command == 'k':
            print("please enter a number for seed generation")
            seedNumber= input("\n")
            random.seed(seedNumber)

            print("your keys")
            keyGenerator()
            print("\n")

        elif command == 'e':
            encryption()
            print("\n")

        elif command == 'd':
            decryption()
            print("\n")

        else:
            print("invalid command entered")
            print("\n")

# --------------------------------------
main()

