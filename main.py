import math
import re

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
        return cipher_text #, cipher_key
    elif mode == DECRYPT_MODE:
        plain_text = ''
        for char in text.upper():
            if char in cipher_key:
                i = cipher_key.index(char)
                plain_text+=A_Z[i]
        return plain_text #, cipher_key

def affine_cipher(mode, text, cipher_key):
    cipher_key=cipher_key.split(',')
    a=int(cipher_key[0].strip())
    text=re.sub('[^'+"".join(a_z)+']*', '', text.lower())
    b=int(cipher_key[1].strip())
    if mode == ENCRYPT_MODE:
        cipher_text = ''
        for char in text.lower():
            if char in a_z:
                m = a_z.index(char)
                i = (a * m + b) % len(a_z)
                cipher_text += a_z[i]
        return cipher_text
    elif mode == DECRYPT_MODE:
        a_inverse = multiplicative_inverse(a, len(a_z))
        plain_text = ''
        for char in text.lower():
            if char in a_z:
                c = a_z.index(char)
                i = (a_inverse * (c-b))%len(a_z)
                plain_text+=a_z[i]
        return plain_text

def play_fair_cipher(mode, text, key):
    text=re.sub('[^'+"".join(A_Z)+']*', '', text.upper()).replace('J', 'I')
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

        return cipher_text #, key
    
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

        return plaintext #, key

def contains_number(input_string):
    for char in input_string:
        if char.isdigit():
            return True
    return False

def vigenere_cipher(mode, text, cipher_key):
    if contains_number(cipher_key):
        cipher_key=[int(x.strip()) for x in cipher_key.split(',')]

    text=re.sub('[^'+"".join(A_Z)+']*', '', text.upper())
    if len(cipher_key) < len(text):
        cipher_key = cipher_key * math.ceil(len(text)/len(cipher_key))
    if type(cipher_key) == str:
        cipher_key=cipher_key.upper()
    else:
        cipher_key = ''.join([A_Z[int(e)] for e in cipher_key])

    if mode == ENCRYPT_MODE:
        cipher_text = ''
        for i in range(len(text)):
            if text[i] in A_Z and cipher_key[i] in A_Z:
                idx=(A_Z.index(text[i]) + A_Z.index(cipher_key[i])) % len(A_Z)
                cipher_text += A_Z[idx]
        return cipher_text
    elif mode == DECRYPT_MODE:
        plain_text = ''
        for i in range(len(text)):
            if text[i] in A_Z and cipher_key[i] in A_Z:
                idx=(A_Z.index(text[i]) - A_Z.index(cipher_key[i])) % len(A_Z)
                plain_text += A_Z[idx]
        return plain_text


def is_binary_string(input_string):
    # Iterate through each character in the string
    for char in input_string:
        # Check if the character is neither '0' nor '1'
        if char != '0' and char != '1':
            return False
    return True

def vernam_cipher(text, cipher_key):
    if is_binary_string(text):
        text = int(text, 2)
    if is_binary_string(cipher_key):
        cipher_key = int(cipher_key, 2)
    
    return bin(text ^ cipher_key)


def rail_fence(mode, text, cipher_key):
    cipher_key=int(cipher_key.strip())
    m = cipher_key # number of rows
    n = math.ceil(len(text)/cipher_key)  # number of columns

    matrix = [['' for _ in range(n)] for _ in range(m)]
    # print(100*"*")
    # print(matrix)
    if mode == ENCRYPT_MODE:
        k=0
        for i in range(n):
            for j in range(cipher_key):
                if k < len(text) :#and i<int(len(text)/cipher_key):
                    matrix[j][i]=text[k]
                    k+=1
        
        cipher_text=''
        for i in range(m):
            cipher_text+=''.join(matrix[i])
        return cipher_text
    elif mode == DECRYPT_MODE:
        k=0
        for i in range(m):
            for j in range(math.ceil(len(text)/cipher_key)):
                if k < len(text) :#and j<int(len(text)/cipher_key):
                    matrix[i][j] = text[k]
                    k+=1
        plain_text=''
        for i in range(n):
            plain_text+=''.join([row[i] for row in matrix])
        return plain_text






import numpy as np

def char_to_index(char):
    return ord(char) - ord('a')

def index_to_char(index):
    return chr(index + ord('a'))

def string_to_numbers(text):
    return [char_to_index(char) for char in text]

def numbers_to_string(numbers):
    return ''.join([index_to_char(num) for num in numbers])

def pad_text(text, key_size):
    padded_text = text
    while len(padded_text) % key_size != 0:
        padded_text += 'x'  # Adding 'x' padding
    return padded_text

def parse_key(key_string):
    key_list = []
    for row in key_string.split(','):
        key_list.append([int(num.strip()) for num in row.split()])
    return key_list

def hill_cipher_encrypt(mode, plaintext, key):
    key = parse_key(key)
    key_size = len(key)
    padded_plaintext = pad_text(plaintext, key_size)
    key_matrix = np.array(key).reshape(int(key_size/2), int(key_size/2))

    encrypted_text = ""
    for i in range(0, len(padded_plaintext), key_size):
        segment = padded_plaintext[i:i+key_size]
        segment_numbers = string_to_numbers(segment)
        segment_matrix = np.array(segment_numbers).reshape(key_size, 1)
        encrypted_segment_matrix = np.dot(key_matrix, segment_matrix) % 26
        encrypted_segment_numbers = encrypted_segment_matrix.flatten().tolist()
        encrypted_segment = numbers_to_string(encrypted_segment_numbers)
        encrypted_text += encrypted_segment

    return encrypted_text

# # Example usage:
# a_z = [chr(i) for i in range(ord('a'), ord('z')+1)]

# plaintext = "hello"
# key_string = '6, 24, 1, 13'
# key = parse_key(key_string)

# encrypted_text = hill_cipher_encrypt(plaintext, key)
# print("Encrypted text:", encrypted_text)








import rsa
def rsa_(mode, text, cipher_key=None):
    p, q = tuple(cipher_key.split(','))
    p=int(p.strip())
    q=int(q.strip())

    if mode == ENCRYPT_MODE:
        return rsa.RSA_Encryption(text, p, q)
    elif mode==DECRYPT_MODE:
        return rsa.RSA_decryption(text, p, q)





from Crypto.Cipher import DES

def pad(text):
    n = len(text) % 8
    return text + (b' ' * n)
def unpad(text):
    return text.rstrip(b' ')





def des_(mode, text, key:str):
    key = key.encode()
    text=text.encode()
    if mode == ENCRYPT_MODE:
        des = DES.new(key, DES.MODE_ECB)
        padded_text = pad(text)
        encrypted_text = des.encrypt(padded_text)
        return encrypted_text
    
    elif mode == DECRYPT_MODE:
        des = DES.new(key, DES.MODE_ECB)
        decrypted_text = des.decrypt(encrypted_text)

        # Remove padding (if any)
        original_text = unpad(decrypted_text)

        return original_text.decode('utf-8')

import hashlib

def sha_1(mode, text, salt=''):
    text+=salt
    # Encode the message to bytes before hashing
    text_bytes = text.encode('utf-8')

    # Create a SHA-1 hash object
    sha1_hash = hashlib.sha1()

    # Update the hash object with the message bytes
    sha1_hash.update(text_bytes)

    # Get the hexadecimal representation of the hash
    hashed_text = sha1_hash.hexdigest()
    return hashed_text


algorithms = {
    1:shift_cipher,
    2:mono_alphabetic_cipher,
    3:affine_cipher,
    4:play_fair_cipher,
    5:vigenere_cipher,
    6:vernam_cipher,
    7:rail_fence,
    8:rsa_,
    9:des_,
    10:sha_1,
    11: hill_cipher_encrypt
}

# Examples
# plain_text = "we will meet at mid night"
# cipher_key = 11

# print(shift_cipher(ENCRYPT_MODE, plain_text, cipher_key))
# print("mono_alphabetic_cipher", mono_alphabetic_cipher(DECRYPT_MODE, "MKJKSIKUP", "EXAMPLE"))
# print(affine_cipher(ENCRYPT_MODE, "hot", (7, 3)))
# print(affine_cipher(DECRYPT_MODE, "axg", (7, 3)))
# print("PlayFair('instruments', 'monarchy')", play_fair_cipher(ENCRYPT_MODE, 'instruments', 'monarchy'))
# print("PlayFair('instruments', 'monarchy')", play_fair_cipher(DECRYPT_MODE, 'GATLMZCLRQXA', 'monarchy'))
# print("vigenere_cipher('tomorrow at the sunset')", vigenere_cipher(ENCRYPT_MODE, 'tomorrow at the sunset', [2, 5, 1, 10, 20]))
# print("vigenere_cipher('tomorrow at the sunset')", vigenere_cipher(DECRYPT_MODE, 'VTNYLTTXKNVMFCOPXFD', [2, 5, 1, 10, 20]))
# print(vernam_cipher("001011010111", "100111001011"))

# print("RAIL FENCE", rail_fence(ENCRYPT_MODE, 'meetmeaftertheparty', 2))
# print("RAIL FENCE", rail_fence(DECRYPT_MODE, 'mematrhpryetefeteat', 2))


from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def enc():
    text = request.form.get('text')
    key = request.form.get('key')
    algo = request.form.get('algo', type=int)
    
    text=algorithms.get(algo)(ENCRYPT_MODE, text, key)
    
    return jsonify({'text':text})

@app.route('/decrypt', methods=['POST'])
def dec():
    text = request.form.get('text')
    key = request.form.get('key')
    algo = request.form.get('algo', type=int)
    
    text=algorithms.get(algo)(DECRYPT_MODE, text, key)
    
    return jsonify({'text':text})

if __name__ == '__main__':
    app.run(debug=True)