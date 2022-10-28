from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode
import base64
import time
import sys
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

def encrypt_EAX(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return (key,cipher.nonce, tag, ciphertext)

def decrypt_EAX(key, nonce, tag, ciphertext):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    descifrado=cipher.decrypt_and_verify(ciphertext, tag)
    return descifrado

def encrypt_CBC(key,data):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return (key,iv,ct)

def decrypt_CBC(key,iv,ct):
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def encrypt_CTR(key,data):
    cipher = AES.new(key, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(data)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return (key,nonce,ct)

def decrypt_CTR(key,nonce,ct):
    nonce = b64decode(nonce)
    ct = b64decode(ct)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ct)
    return pt

with open("HIPODONCIA_DENTAL.jpg", "rb") as imageFile:
    hipodoncia = base64.b64encode(imageFile.read())
    key_hipodoncia= get_random_bytes(16)
    inicio=time.time()
    encript=encrypt_CBC(key_hipodoncia,hipodoncia)
    fin=time.time()
    print("Tiempo de ejecucion cifrado CTR:")
    print(fin-inicio)
    print("Tamaño de cifrado EAX:")
    print(sys.getsizeof(encript[2]))
    print("Tiempo de ejecucion descifrado CTR:")
    inicio=time.time()
    desencript = decrypt_CBC(encript[0],encript[1],encript[2])
    fin=time.time()
    print(fin-inicio)
    print("Tamaño de descifrado EAX:")
    print(sys.getsizeof(desencript))


