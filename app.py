
P10 = [2,4,1,6,3,9,0,8,7,5]
P8  = [5,2,6,3,7,4,9,8]
IP  = [1,5,2,0,3,7,4,6]
IP_INV = [3,0,2,4,6,1,7,5]
EP  = [3,0,1,2,1,2,3,0]
P4  = [1,3,2,0]

S0 = [
    [1,0,3,2],[3,2,1,0],
    [0,2,1,3],[3,1,3,2]
]
S1 = [
    [0,1,2,3],[2,0,1,3],
    [3,0,1,0],[2,1,0,3]
]

def permute(bits, table):
    return ''.join(bits[i] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_keys(key10):
    p10 = permute(key10, P10)
    left, right = p10[:5], p10[5:]
    ls1 = left_shift(left,1) + left_shift(right,1)
    k1 = permute(ls1, P8)
    ls2 = left_shift(ls1[:5],2) + left_shift(ls1[5:],2)
    k2 = permute(ls2, P8)
    return k1, k2

def f_function(right4, key8):
    ep = permute(right4, EP)
    xor_res = ''.join('1' if ep[i]!=key8[i] else '0' for i in range(8))
    l4, r4 = xor_res[:4], xor_res[4:]
    # S0
    row = int(l4[0]+l4[3],2)
    col = int(l4[1]+l4[2],2)
    s0 = f"{S0[row][col]:02b}"
    # S1
    row = int(r4[0]+r4[3],2)
    col = int(r4[1]+r4[2],2)
    s1 = f"{S1[row][col]:02b}"
    return permute(s0+s1,P4)

def decrypt_verbose(cipher8, key10):
    print(f"Криптограма {cipher8}")
    k1, k2 = generate_keys(key10)
    print(f"K1: {k1}")
    print(f"K2: {k2}")
    # IP
    ip = permute(cipher8, IP)
    print(f"IP {ip}")
    L, R = ip[:4], ip[4:]
    f1 = f_function(R, k2)
    L1 = ''.join('1' if L[i]!=f1[i] else '0' for i in range(4))
    step1 = L1 + R
    print(f"Після FK1  {step1}")
    swapped = R + L1
    print(f"Після SW {swapped}")
    Ls, Rs = swapped[:4], swapped[4:]
    f2 = f_function(Rs, k1)
    L2 = ''.join('1' if Ls[i]!=f2[i] else '0' for i in range(4))
    step2 = L2 + Rs
    print(f"Після FK2 (з K1) {step2}")
    # 1IP⁻¹
    final = permute(step2, IP_INV)
    print(f"Після 1IP-1  {final}")
    print(f"У десятковому вигляді {int(final,2)}")

if __name__ == "__main__":
    cipher = input("Введіть криптограму 8 біт ").strip()
    decrypt_verbose(cipher, "0011011101")
