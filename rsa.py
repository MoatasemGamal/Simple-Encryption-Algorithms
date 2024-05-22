import math



# print("n : ",n)
# print("fi_of_n : ",fi_of_n)

# compute e


        
# print('e = ', e)

# compute d ==> e^-1
def compute_d (e,fi_of_n):
    
    for i in range(1,fi_of_n):
        num = i*e
        if(num%fi_of_n) == 1:
            out = i
    return out


# print('d = ', d)


# print("e : ",e)
# print("d : ",d)


def RSA_Encryption(message, p, q):
    # p = 13
    # q = 61

    n = p*q
    fi_of_n = (p-1)*(q-1)
    
    for i in range(2,fi_of_n):
        if math.gcd(i,fi_of_n) == 1:
            e = i
            break
    
    C=[]
    for i in message:
        i = ord(i)
        c = (i**e)% n
        C.append(chr(c))
    return C

def RSA_decryption(Cipher, p, q):
    # p = 13
    # q = 61

    n = p*q
    fi_of_n = (p-1)*(q-1)

    for i in range(2,fi_of_n):
        if math.gcd(i,fi_of_n) == 1:
            e = i
            break
    
    d = compute_d(e,fi_of_n)   #(e**-1)% fi_of_n
    T=[]
    for i in Cipher:
        i = ord(i)
        t = (i**d) % n
        T.append(chr(t))
    return T

#m = int(input("Enter a number"))
#c = (m**e)% n
#t = (c**d) % n

# m = input("Enter a Character : ")
# C = []
# T = []


# print("you Entered : ",m)
# C = RSA_Encryption(m)
# T = RSA_decryption(C)



# print("your cipher text is : ","".join(C))
# print("your text again  is : ","".join(T))



# print("you Entered : ",m)
# C = RSA_Encryption(m)
# T = RSA_decryption(C)



# print("your cipher text is : ","".join(C))
# print("your text again  is : ","".join(T))




# print("you Entered : ",m)
# C = RSA_Encryption(m)
# T = RSA_decryption(C)



# print("your cipher text is : ","".join(C))
# print("your text again  is : ","".join(T))


