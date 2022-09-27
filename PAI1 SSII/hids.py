import envia_email
import hashlib
import os
import time
import logging

#Configuración de la gestión del Log
logging.basicConfig(filename='registro.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

#Establecer variables del sistema
#TO DO: RECUPERAR LA RUTA DE UN ARCHIVO EXTERNO AL SCRIPT, QUE SERÁ NUESTRO ARCHIVO DE CONFIGURACIÓN
DIRECTORIO_BASE = "C:/Users/nicos/Desktop/IDOM"
PERIODO = 10.0 #PERIODO EN SEGUNDOS
REPORTE = 30 #CADA CUANTOS CHECKEOS SE MANDA UN REPORTE 

"""
Implementación de la clase de arbol binario. Cada nodo representa un archivo
y tiene un atributo ID único, un atributo path, que contiene la ruta de ese archivo, 
un atributo hash, que contiene el hash del archivo, y dos atributos left y right que
constituyen sus nodos hijos. El árbol que generaremos posteriormente será un arbol
binario de búsqueda, que además estará balanceado, de tal forma que un recorrido
"in orden" del arbol devolvería los IDs ordenados perfectamente de menor a mayor
"""
class BinaryTree:
    def __init__(self, ID):
        self.ID = ID
        self.path = None
        self.hash = None
        self.left = None
        self.right = None
        
"""
Función que obtiene el hash de un archivo. Utiliza un tamaño de buffer de 64KB
para evitar colapso de memoria con archivos grandes
"""
def getFileHash(path, buffer_size = 65536):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

"""
Función que obtiene una lista con todas las rutas de los archivos a proteger
"""
def getAllFilesInDirectory(mainPath, files = []):
    for myPath in os.listdir(mainPath):
        newPath = mainPath+'/'+myPath
        if not (os.path.isfile(newPath)):
            getAllFilesInDirectory(newPath)
        else:
            files.append(newPath)
    return files


"""
Función que crea arbol binario de busqueda completamente balanceado a partir de una
lista ordenada con todos los ids,
una lista con todas las rutas a los archivos, y dos valores usados en la recursividad del algoritmo
"""
def createBST(ids, files, a, b): 
    if a > b: return    #Caso base de la recursividad
    mid = (a+b)//2      #Calcula el punto medio de la lista de ids
    root = BinaryTree(mid)
    root.left = createBST(ids, files, a, mid-1)
    root.right = createBST(ids, files, mid+1, b)
    root.path = files[mid]
    root.hash = getFileHash(files[mid])
    return root

"""
Función para hacer una búsqueda optimizada en el arbol generado
"""
def searchFileById(root, ID):
    if ID == root.ID:
        return root
    elif ID < root.ID:
        return searchFileById(root.left, ID)
    elif ID > root.ID:
        return searchFileById(root.right, ID)

"""
Función que comprueba si ha sido comprometida la integridad de los archivos que se le pasan
"""
def checkIntegrity(tree, ids):
    compromisedFiles = []
    nameFile = ""
    for i in ids:
        node = searchFileById(tree, i)
        newHash = getFileHash(node.path)
        if newHash != node.hash:
            compromisedFiles.append(node.path)
            nameFile = os.path.basename(node.path)
            logging.debug(nameFile)                     #si y solo si se produce una modificación se guarda en el log

    if compromisedFiles != []:
        print("Compromised files:", compromisedFiles)
    return compromisedFiles
        
if not os.path.exists(DIRECTORIO_BASE):
    print("D")
    raise Exception("La ruta especificada no existe")
files = getAllFilesInDirectory(DIRECTORIO_BASE)
n = len(files)
print("Construyendo árbol binario de búsqueda de {} archivos".format(n))
timer = time.perf_counter()
tree = createBST(list(range(n)), files, 0, n-1)
print("¡Hecho en {} segundos!".format(time.perf_counter() - timer))

starttime = time.time()
k = 0
while True:
    print("tick")
    checkIntegrity(tree, list(range(n)))
    print(PERIODO - ((time.time() - starttime)  % PERIODO))
    time.sleep(PERIODO - ((time.time() - starttime) % PERIODO))
    if (k == REPORTE):
        print("REPORTE")
        #envia_email
        k = 0
    k+=1

"""      
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

print(integrity(DIRECTORIO_BASE))
"""
