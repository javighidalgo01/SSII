import secrets
import hmac
import random
import pathlib
import os

project_path = pathlib.Path(__file__).parent.parent.resolve()
nonce_path = os.path.join(project_path, "nonceHistory.txt")

def secureMessage(text, key):
    nonce = getNonce()
    textB = (text + ' ' + nonce).encode()
    mac = hmac.new(key, msg = textB, digestmod = 'sha256')
    digest = mac.digest()
    return textB + digest

def mitm(message):
    mac = message[-32:]
    mensaje_con_nonce = message[:-32]
    mensaje_cliente = mensaje_con_nonce[:-21]
    nonce = mensaje_con_nonce[-21:]
    return mensaje_cliente+ " MOD".encode() + nonce + mac

def updateSecretKey():
    global secretKey, secretKeySet
    secretKey = secrets.token_bytes(16)
    secretKeySet=True

def toStrFixedLength(length, num):
    return "0" * (length - len(str(num))) + str(num)

def getNonce():
    nonce = toStrFixedLength(20, secrets.randbelow(10**20))
    try:
        with open(nonce_path, 'rt') as f:
            while nonce in f.readlines():
                nonce = toStrFixedLength(20, secrets.randbelow(10**20))                             
    except OSError as e:
        print("No se ha podido comprobar si el nonce se ha generado anteriormente:", e.strerror)
        if  e.errno == 2:
            print("El motivo es que el archivo no existe. Se intentara crear...")
            with open(nonce_path, 'x') as f:
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
    with open(nonce_path, 'a') as f:
        f.write(nonce+"\n")

def nonceHaSidoUsado(nonce):
    try:
        with open(nonce_path, 'rt') as f:
            return nonce in f.read().splitlines()                         
    except OSError as e:
        print("No se ha podido acceder al historial de nonces. Servidor vulnerable a ataque replay.", e.errno, e.strerror)

def check_mitm(mensaje, oldDigest):
    mac_nuevo = hmac.new(secretKey, msg = mensaje, digestmod = 'sha256')
    return mac_nuevo.digest() != oldDigest

updateSecretKey()

"""
def write_to_log(file_object, event_name, description):
    event_time = str(datetime.datetime.now())
    data = OrderedDict()
    data['time'] = event_time
    data['event'] = event_name
    data['details'] = description
    json.dump(data, file_object, separators=(', ', ':'))
    file_object.write('\n')
"""



