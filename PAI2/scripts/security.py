import secrets
import hmac

secretKey = None
secretKeySet = False
mac= ""
nonce = ""

def secureMessage(text, key):
    global mac,nonce
    nonce = getNonce()
    text += nonce
    textB = text.encode()
    mac = hmac.new(key, msg=textB, digestmod='sha256')
    digest = mac.digest()
    return textB +" ".encode()+ digest
    
    
def updateSecretKey():
    global secretKey, secretKeySet
    secretKey = secrets.token_bytes(16)
    secretKeySet=True

def man_in_the_middle(mensaje):
    mac_nuevo=hmac.new(secretKey, msg=mensaje.split()[0], digestmod='sha256')
    print(mensaje)
    if(mac_nuevo.digest()!=mac.digest()):
        return False
    else:
        return True

def toStrFixedLength(length, num):
    nonceStr = str(num)
    for _ in range(length - len(nonceStr)):
        nonceStr = "0" + nonceStr
    return nonceStr

def getNonce():
    nonce = toStrFixedLength(20, secrets.randbelow(10**20))
    try:
        with open("nonceHistory.txt", 'rt') as f:
            while nonce in f.readlines():
                nonce = toStrFixedLength(20, secrets.randbelow(10**20))                             
    except OSError as e:
        print("No se ha podido comprobar si el nonce se ha generado anteriormente", e.errno, e.strerror)
    return nonce

if not secretKeySet:
    updateSecretKey()

print(nonce,mac)