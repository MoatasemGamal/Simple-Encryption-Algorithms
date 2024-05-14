ENCRYPT_MODE = 'encrypt'
DECRYPT_MODE = 'decrypt'

a_z = list('abcdefghijklmnopqrstuvwxyz')
A_Z = list('abcdefghijklmnopqrstuvwxyz'.upper())

#============================================================================================

def u(l):
    unique_elements = []
    for x in l:
        if x not in unique_elements:
            unique_elements.append(x)
    return unique_elements
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def multiplicative_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"The multiplicative inverse of {a} modulo {m} does not exist.")
    else:
        return x % m
    
#============================================================================================


def shift_cipher(mode, text, cipher_key):
    if mode == ENCRYPT_MODE:
        cipher_text = ''
        for char in text.lower():
            if char in a_z:
                c_index = a_z.index(char)
                i = (c_index+int(cipher_key)) % len(a_z)
                cipher_text+=a_z[i]
        return cipher_text
    elif mode == DECRYPT_MODE:
        plain_text = ''
        for char in text.lower():
            if char in a_z:
                c_index = a_z.index(char)
                i = (c_index-int(cipher_key)) % len(a_z)
                plain_text+=a_z[i]
        return plain_text

def mono_alphabetic_cipher(mode, text, cipher_key:str):
    cipher_key = u(u(cipher_key.upper()) + A_Z)
    if mode == ENCRYPT_MODE:
        cipher_text = ''
        for char in text.upper():
            if char in A_Z:
                i = A_Z.index(char)
                cipher_text+=cipher_key[i]
        return cipher_text, cipher_key
    elif mode == DECRYPT_MODE:
        plain_text = ''
        for char in text.upper():
            if char in cipher_key:
                i = cipher_key.index(char)
                plain_text+=A_Z[i]
        return plain_text, cipher_key

def affine_cipher(mode, text, cipher_key:tuple):
    a=cipher_key[0]
    a_inverse = multiplicative_inverse(a, len(a_z))
    b=cipher_key[1]
    if mode == ENCRYPT_MODE:
        cipher_text = ''
        for char in text.lower():
            if char in a_z:
                m = a_z.index(char)
                i = (a * m + b) % len(a_z)
                cipher_text += a_z[i]
        return cipher_text
    elif mode == DECRYPT_MODE:
        plain_text = ''
        for char in text.lower():
            if char in a_z:
                c = a_z.index(char)
                i = (a_inverse * (c-b))%len(a_z)
                plain_text+=a_z[i]
        return plain_text




# Examples
plain_text = "we will meet at mid night"
cipher_key = 11

print(shift_cipher(ENCRYPT_MODE, plain_text, cipher_key))
print("mono_alphabetic_cipher", mono_alphabetic_cipher(DECRYPT_MODE, "MKJKSIKUP", "EXAMPLE"))
print(affine_cipher(ENCRYPT_MODE, "hot", (7, 3)))
print(affine_cipher(DECRYPT_MODE, "axg", (7, 3)))



