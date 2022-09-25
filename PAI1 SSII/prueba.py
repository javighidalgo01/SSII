import hashlib
import os
import time
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
                    result.update({i.name : m.hexdigest()})    
    return result

hashes_de_archivos = generador_de_hash(DIRECTORIO_BASE)

time.sleep(15)

def integrity(DIRECTORIO_BASE):
    result = ""
    hash_nuevo=generador_de_hash(DIRECTORIO_BASE)
    for i , z in hashes_de_archivos.items():
        if(z!=hash_nuevo.get(i)):
            print("Hash antes de modificar el archivo "+i, z)
            result = result + "Ataque a la integridad en el archivo "+ i
            print("Nuevo hash tras la modificación del archivo: "+i, hash_nuevo.get(i))   
    return result

print(integrity(DIRECTORIO_BASE))
