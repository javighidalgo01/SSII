from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import hashlib
import base64

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
    key_hipodoncia= b'1222222222332335'
    encript=encrypt_CTR(key_hipodoncia,hipodoncia)
    imagen = hashlib.sha512()
    imagen.update(hipodoncia)
    imagen = imagen.hexdigest()
    print("Hash imagen\n"+imagen)
    desencript = decrypt_CTR(encript[0],encript[1],encript[2])
    descifrada = hashlib.sha512()
    descifrada.update(desencript)
    descifrada = descifrada.hexdigest()
    print("Hash imagen descifrada\n"+descifrada)