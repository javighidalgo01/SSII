import pathlib
import os

conf_loaded = False
script_path = pathlib.Path(__file__).parent.parent.resolve()
parameters_filename = "PARAMETERS.conf"
parameters_path = os.path.join(script_path, parameters_filename)

def loadHIDS():
    try:
        with open(parameters_path, 'rt') as f:
            #obtenemos los 3 primeros parámetros del archivo de configuración
            #dividiendo la línea por el caracter '=', quedándonos con el segundo trozo,
            #quitando los comentarios de la linea (dividiendo por el caracter '#'),
            #y quitando los espacios con la función strip()            
            params = [l.split('=')[1].split('#')[0].strip() for l in f.readlines()[0:3]]

        if params[0] == "default":
            DIRECTORIO_BASE = str(pathlib.Path.home()) + "/Protected"
        else:
            DIRECTORIO_BASE = params[0]
        
        return (DIRECTORIO_BASE, float(params[1]), int(params[2]))
                                
    except OSError as e:
        print("No se ha podido abrir el fichero de configuración")
        raise e
    
def loadMail():
    
    try:
        with open(parameters_path, 'rt') as f:
            params = [l.split('=')[1].split('#')[0].strip() for l in f.readlines()[3:11]]
            destinatarios = [d.strip() for d in params[5].split(',')]
        
        return (params[0], params[1], params[2], params[3], int(params[4]), destinatarios, params[6],params[7])
                                
    except OSError as e:
        print("No se ha podido abrir el fichero de configuración")
        raise e
    