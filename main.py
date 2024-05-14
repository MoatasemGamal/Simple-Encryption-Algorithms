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

plain_text = "we will meet at mid night"
cipher_key = 11



# Examples
print(shift_cipher(ENCRYPT_MODE, plain_text, cipher_key))
