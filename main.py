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
    
def find_char_positions(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
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

def play_fair_cipher(mode, text, key):
    text = text.upper().replace('J', 'I').replace(' ','') 
    key = u(key.upper().replace('J', 'I').replace(' ',''))
    A_Z_without_j = A_Z.copy()
    A_Z_without_j[A_Z_without_j.index('J')] = 'I'
    key = u(key + A_Z_without_j)
    
    matrix = [['' for _ in range(5)] for _ in range(5)]
    key_index = 0
    for i in range(5):
        for j in range(5):
            if key_index < len(key):
                if key[key_index] in A_Z_without_j:
                    matrix[i][j] = key[key_index]
                key_index+=1

    if mode == ENCRYPT_MODE:
        plain_text = text
        plaintext_pairs = []
        i = 0
        while i < len(plain_text):
            if i == len(plain_text) - 1 or plain_text[i] == plain_text[i + 1]:
                plaintext_pairs.append(plain_text[i] + 'X')
                i += 1
            else:
                plaintext_pairs.append(plain_text[i] + plain_text[i + 1])
                i += 2

        # Encrypt pairs
        cipher_text = ""
        for pair in plaintext_pairs:
            char1, char2 = pair[0], pair[1]
            row1, col1 = find_char_positions(matrix, char1)
            row2, col2 = find_char_positions(matrix, char2)

            if row1 == row2:
                cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                cipher_text += matrix[row1][col2] + matrix[row2][col1]

        return cipher_text, key
    
    elif mode == DECRYPT_MODE:
        cipher_text = text
        plaintext = ""
        for i in range(0, len(cipher_text), 2):
            char1, char2 = cipher_text[i], cipher_text[i + 1]
            row1, col1 = find_char_positions(matrix, char1)
            row2, col2 = find_char_positions(matrix, char2)

            if row1 == row2:
                plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                plaintext += matrix[row1][col2] + matrix[row2][col1]

        return plaintext, key


# Examples
plain_text = "we will meet at mid night"
cipher_key = 11

print(shift_cipher(ENCRYPT_MODE, plain_text, cipher_key))
print("mono_alphabetic_cipher", mono_alphabetic_cipher(DECRYPT_MODE, "MKJKSIKUP", "EXAMPLE"))
print(affine_cipher(ENCRYPT_MODE, "hot", (7, 3)))
print(affine_cipher(DECRYPT_MODE, "axg", (7, 3)))
print("PlayFair('instruments', 'monarchy')", play_fair_cipher(ENCRYPT_MODE, 'instruments', 'monarchy'))
print("PlayFair('instruments', 'monarchy')", play_fair_cipher(DECRYPT_MODE, 'GATLMZCLRQXA', 'monarchy'))



