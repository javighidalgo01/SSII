from datetime import date
import secrets
import hmac
import random
import json
import datetime
from collections import OrderedDict


secretKey = None
secretKeySet = False

def secureMessage(text, key):
    nonce = getNonce()
    textB = (text + ' ' + nonce).encode()
    mac = hmac.new(key, msg = textB, digestmod = 'sha256')
    digest = mac.digest()
    return textB + digest

def random_Mitm(mensaje_cliente,nonce):
    i = random.choice(range(2))
    if(i==1):
        return mensaje_cliente+"b "+nonce
    else:
        return mensaje_cliente+nonce

def updateSecretKey():
    global secretKey, secretKeySet
    secretKey = secrets.token_bytes(16)
    secretKeySet=True

def toStrFixedLength(length, num):
    return "0" * (length - len(str(num))) + str(num)

def getNonce():
    nonce = toStrFixedLength(20, secrets.randbelow(10**20))
    try:
        with open("nonceHistory.txt", 'rt') as f:
            while nonce in f.readlines():
                nonce = toStrFixedLength(20, secrets.randbelow(10**20))                             
    except OSError as e:
        print("No se ha podido comprobar si el nonce se ha generado anteriormente:", e.strerror)
        if  e.errno == 2:
            print("El motivo es que el archivo no existe. Se intentara crear...")
            with open("nonceHistory.txt", 'x') as f:
                f.close()
                print("Exito al crear")
    return nonce

def generaMensaje():
    origen = ""
    destino = ""
    cantidad = ""
    for x in range(5): 
        origen += str(random.randint(0,9))
        destino += str(random.randint(0,9))
    for y in range(3):
        cantidad += str(random.randint(0,9))

    return origen + " " + destino + " " + cantidad


def agregaNonceAlRegistro(nonce):
    #se escribe el nonce en el fichero nonceHistory.
    with open("nonceHistory.txt", 'a') as f:
        f.write(nonce+"\n")

def nonceHaSidoUsado(nonce):
    try:
        with open("nonceHistory.txt", 'rt') as f:
            return nonce in f.readlines()                            
    except OSError as e:
        print("No se ha podido acceder al historial de nonces. Servidor vulnerable a ataque replay.", e.errno, e.strerror)

def check_man_in_the_middle(mensaje, oldDigest):
    mac_nuevo = hmac.new(secretKey, msg = mensaje, digestmod = 'sha256')
    return mac_nuevo.digest() != oldDigest

if not secretKeySet:
    updateSecretKey()

def write_to_log(file_object, event_name, description):
    """Write message to a log file"""
    event_time = str(datetime.datetime.now())
    data = OrderedDict()
    data['time'] = event_time
    data['event'] = event_name
    data['details'] = description
    json.dump(data, file_object, separators=(', ', ':'))
    file_object.write('\n')