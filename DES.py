def hex2bin(string: str):
    mp = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }
    bin =""
    for i in range(len(string)):
        bin += mp[string[i]]
        
    return bin 
print(hex2bin("123456789ABCDEF"))


def bin2hex(string: str):
    mp = {
        '0000': '0',
        '0001': '1',
        '0010': '2',
        '0011': '3',
        '0100': '4',
        '0101': '5',
        '0110': '6',
        '0111': '7',
        '1000': '8',
        '1001': '9',
        '1010': 'A',
        '1011': 'B',
        '1100': 'C',
        '1101': 'D',
        '1110': 'E',
        '1111': 'F'
    }
    # 1101010
    hex = ""
    for i in range(0,len(string),4):
        ch =""
        ch += string[i]
        ch += string[i+1]
        ch += string[i+2]
        ch += string[i+3]
        hex += mp[ch]
        
    return hex


def bin2dec(binary: str) -> int:
    dec = 0
    power = len(binary) - 1
    
    for bit in binary:
        if bit == '1':
            dec += 2 ** power
        power -= 1
    
    return dec


def dec2bin(num):
    res = bin(num).replace("0b", "")
    if len(res) % 4 != 0:
        div = len(res) // 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

def permute(input_val, box):
    permutation = ""
    for i in range(0,len(box)):
        permutation += input_val[box[i] - 1]
    return permutation



def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s=""

    return k
                
def xor(a,b):
    ans =""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans += "0"
        else:
            ans += "1"
    return ans

pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

shift_table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

k_bin = "133457799BBCDFF1"
k = hex2bin(k_bin)

print("* "*17, "Key Generation", "* "*17,"\n")

print('Key Before passing to PC_1:',k)

#getting 56 bit key from 64 bit using the parity bits

#Passing key through PC_1

key = permute(k, pc1)

print('Key After passing to PC_1', key)

left  = key[0:28] # rkb for RoundKeys in binary right key [28:56] #rk for RoundKeys in hexadecimal
right = key[28:56]
rkb = []

rk = []

print("\n","* "*17, "Splitting", " "*17)

for i in range(0, 16):
    print("*", "Round: ",1+1, "* "*17)

    print("L"+str(1+1),": \t\t\t\t", left)

    print("R"+str(i+1),": \t\t\t\t", right)

    #Shifting the bits by nth shifts by checking from shift table

    left = shift_left(left, shift_table[i]) 
    right = shift_left(right, shift_table[i])

    print("L"+str(1+1)," After ", shift_table[i]," shift: \t\t", left) 
    print("R"+str(i+1)," After ", shift_table[i]," shift \t\t", right)

    #Combination of Left and right string 
    combine_str = left + right

    print("L"+str(1+1)," R"+str(1+1)," : \t\t\t",combine_str)

    #Compression of key from 56 to 48 bits using PC_2 
    round_key = permute(combine_str, pc2)

    # print("L"+str(i+1)," R"+str(1+1)," After PC_2 \t\t", round_key) 
    rkb.append(round_key)

    # print(rkb)
    #rk.append(bin2hex(round_key))
    
initial_perm =[58, 50, 42, 34, 26, 18, 18, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    
E_Bit = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

sbox = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 8, 6, 9, 0, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 8, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 0, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 1, 4, 25]

final_perm = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 
              53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

def encrypt(pt, key):
    key=rkb
    pt = hex2bin(pt)
    print("Plain Text in Binary :\t\t", pt)
    print(len(pt))

    
    # initial permutation 
    pt = permute(pt, initial_perm)
    print("After initial permutation(ip)", pt)

    left = pt[0:32]
    right = pt[32:64]
    print("L0 \t\t\t", left)
    print("R0 \t\t\t", right)
    print("\n", "* " * 7, "Computation of L_n R_(n-1), R_n L_(n-1) + F(R_(n-1), K_n)", "* " * 7)

    for i in range(0, 16):
        print("\n", "* " * 17, "Round: ", str(i + 1), "* " * 17)
        
        print("\n", "* " * 4, "Expansion D-box: Expanding the 32 bits data into 48 bits", "* " * 4, "\n")

        # Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, E_Bit)
        
        print("R", str(i), ": \t\t\t\t", right)
        print("E(R)", str(i), " 32 --> 48:\t\t", right_expanded)

        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])

        print("X", str(i + 1), ": \t\t\t", rkb[i])

        print("\t\t\t\t", "-" * 50)

        print("f(R_(n-1)+K_n)", "\t\t", xor_x, "\n")

        # S-boxes: substituting the value from s-box table by calculating row and column
        sbox_str = ""

        for j in range(0, 8):
            row = bin2dec(xor_x[j * 6] + xor_x[j * 6 + 5])
            col = bin2dec(
                xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4])

            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)

        print("S1(B1)S2(B2)...S8(B8)", ": \t", sbox_str)

        # Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, P)

        print("P(S1(B1)S2(B2)...S8(B8))", ": \t", sbox_str, "\n")

        # XOR Left and sbox_str
        result = xor(left, sbox_str)

        left = result

        print("Left", i + 1, ": \t\t\t", left)
        print("Right", i + 1, ":\t\t\t", right)

        # Swapper
        if i != 15:
            left, right = right, left

        print("Final Result of Round ", i + 1, "\t", left, " ", right)

    # Combine left and right
    combine = left + right

    print("R16L16 : \t\t\t", combine)

    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm)

    print("IP-1(R16L16): \t\t\t", cipher_text)

    return cipher_text

# pt = "123456789ABCDEF"

# cipher_text = (encrypt(pt,rkb))

# print(cipher_text)

