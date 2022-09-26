
import smtplib
import hashlib
import os
import time

import logging


#Establecer variables del sistema
user = "juahurmas@alum.us.es"
passW = "HHpitt66...." 
server = "mail.us.es"
puerto = 587

#Función de envío de mail
def envioMail (recipient, subject, text):
    smtpserver = smtplib.SMTP(server, puerto)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(user, passW)
    header = 'To: '+recipient+ "\n" + "From: "+user
    header = header + "\n" + "Subject:" +subject+ "\n"
    msg = header + "\n" + text + "\n\n"
    smtpserver.sendmail(user, recipient, msg)
    smtpserver.close()

envioMail("juanpepitt@gmail.com", "sub", "Este es un correo desde python para la practica de SSII PAI1")

DIRECTORIO_BASE = "C:/Users/juanp/Desktop/IDOM"

def generador_de_hash(DIRECTORIO_BASE):
    result = {}
    for i in os.scandir(DIRECTORIO_BASE):
        if os.path.isdir(i):
            carpeta = DIRECTORIO_BASE+"/"+i.name
            result.update(generador_de_hash(carpeta))
        else:
            m = hashlib.sha256()
            with open(i, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    m.update(bloque)
                    result[i.name] = m.hexdigest()    
    return result

hashes_de_archivos = generador_de_hash(DIRECTORIO_BASE)

time.sleep(15)

def integrity(DIRECTORIO_BASE):
    result = ""
    hash_nuevo=generador_de_hash(DIRECTORIO_BASE)
    for i , z in hashes_de_archivos.items():
        if(z!=hash_nuevo[i]):


            print("Hash antes de modificar el archivo "+i, z)
            result = result + "Ataque a la integridad en el archivo "+ i
            print("Nuevo hash tras la modificación del archivo: "+i, hash_nuevo.get(i))   
    return result

print(integrity(DIRECTORIO_BASE))


def generaLog():
    LOG_FILENAME = 'logging_example.out'
    logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
    )

    logging.debug('This message should go to the log file')

    with open(LOG_FILENAME, 'rt') as f:
        body = f.read()

    print('FILE:')
    print(body)