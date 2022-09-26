import envia_email
import hashlib
import os
import time
import logging

#Configuración de la gestión del Log
logging.basicConfig(filename='registro.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

#########################################################################################################################################################

DIRECTORIO_BASE = "ruta"

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

#########################################################################################################################################################

def integrity(DIRECTORIO_BASE):
    result = ""
    hash_nuevo=generador_de_hash(DIRECTORIO_BASE)
    for i , z in hashes_de_archivos.items():
        if(z!=hash_nuevo[i]):

            #print("Hash antes de modificar el archivo "+i, z)
            result = result + "Ataque a la integridad en el archivo "+ i
            #print("Nuevo hash tras la modificación del archivo: "+i, hash_nuevo[i])   
            logging.debug(result)      #si y solo si se produce una modificación se guarda en el log
    return result

integrity(DIRECTORIO_BASE)