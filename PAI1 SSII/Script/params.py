from pathlib import Path

conf_loaded = False

def loadHIDS():
    try:
        with open("PARAMETERS.conf", 'rt') as f:
            #obtenemos los 3 primeros parámetros del archivo de configuración
            #dividiendo la línea por el caracter '=', quedándonos con el segundo trozo,
            #quitando los comentarios de la linea (dividiendo por el caracter '#'),
            #y quitando los espacios con la función strip()            
            params = [l.split('=')[1].split('#')[0].strip() for l in f.readlines()[0:3]]

        if params[0] == "default":
            DIRECTORIO_BASE = str(Path.home()) + "/Protected"
        else:
            DIRECTORIO_BASE = params[0]
        
        return (DIRECTORIO_BASE, float(params[1]), int(params[2]))
                                
    except OSError as e:
        print("No se ha podido abrir el fichero de configuración")
        raise e
    
def loadMail():
    
    try:
        with open("PARAMETERS.conf", 'rt') as f:
            params = [l.split('=')[1].split('#')[0].strip() for l in f.readlines()[3:11]]
            destinatarios = [d.strip() for d in params[4].split(',')]
        
        return (params[0], params[1], params[2], int(params[3]), destinatarios, params[5], params[6],params[7])
                                
    except OSError as e:
        print("No se ha podido abrir el fichero de configuración")
        raise e
    