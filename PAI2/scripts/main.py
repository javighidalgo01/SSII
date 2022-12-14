import socket
import logging
import random
import threading
import socket
import security
import pathlib
import os
import time

'''
VARIABLES AJUSTABLES
'''
mensajes_enviados = 500
prob_mitm = 0.5
prob_replay = 0.1

#Configuracion del log 
assert prob_mitm + prob_replay <=1 and prob_mitm > 0 and prob_replay > 0
project_path = pathlib.Path(__file__).parent.parent.resolve()
register_path = os.path.join(project_path, "registro.log")
logging.basicConfig(filename=register_path, format='%(asctime)s - %(message)s', level=logging.DEBUG)
stream_lock = threading.Lock()
kpi = []
n_ataques_replay_generados = 0
n_ataques_mitm_generados = 0

def write_to_log(event_name, description):
    logging.debug(event_name+" - "+description)

def ataqueReplayDetectado(mensaje_cliente, nonce):
    #print("Transaction Denied: Nonce ya usado (Ataque Replay)")
    write_to_log("Ataque Replay","Mensaje: "+mensaje_cliente+ "      - El nonce "+nonce+" ya ha sido usado")
    kpi.append("RP")

def ataqueMITMDetectado(mensaje_cliente):
    #print("Transaction Denied: Mac distinta Cliente/Servidor (Ataque MITM)")
    write_to_log("Ataque MITM  ","Mensaje: "+mensaje_cliente + "  - Los codigos MAC no coinciden")
    kpi.append("MITM")

'''
Funcion que implementa el servidor con su logica.
Primero abre la conexion que se queda abierta mientras reciba mensajes.
Para cada mensaje, comprueba si ha sido fruto de un ataque mitm
o un ataque replay, y en tal caso, registra el incidente en el log
'''
def server_func():
    host = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 5005))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        
        mensaje_con_nonce = data[:-32]
        mensaje_cliente = mensaje_con_nonce[:-21].decode()
        nonce = mensaje_con_nonce[-20:].decode()
        macDigest = data[-32:]
        stream_lock.acquire() #esto solo hace falta para hacer print. Si en el futuro quitamos los print podemos quitar esta linea
        #print("Received:", mensaje_cliente)
        if security.nonceHaSidoUsado(nonce):    
            ataqueReplayDetectado(mensaje_cliente, nonce)
            conn.send("FAILED".encode())
        elif security.check_mitm(mensaje_con_nonce, macDigest):
            ataqueMITMDetectado(mensaje_cliente)
            conn.send("FAILED".encode())
        else:
            #print("Transaction Accepted")
            security.agregaNonceAlRegistro(nonce)
            conn.send("OK".encode())
        stream_lock.release()#esto solo hace falta para hacer print. Si en el futuro quitamos los print podemos quitar esta linea
        
    conn.close()
    
    print("\nMensajes generados en total: {}.\nProbabilidad MITM: {}. Probabilidad replay: {}".format(mensajes_enviados, prob_mitm, prob_replay))
    print("Se han generado {} ataques MITM. De los cuales detectados: {}".format(n_ataques_mitm_generados, str(kpi.count('MITM'))))
    print("Se han generado {} ataques Replay. De los cuales detectados: {}".format(n_ataques_replay_generados, str(kpi.count('RP'))))
    print("KPI: "+str(len(kpi)/mensajes_enviados))


'''
Funcion que implementa el cliente. Abre la conexion y genera tantos mensajes como se
haya especificado en las variables globales. Ademas, segun las probabilidades
especificadas, simula ambos tipos de ataque, modificando el mensaje en el caso
del ataque MITM, y mandando dos veces exactamente el mismo mensaje en el caso de ataque replay
'''
def client_func():
    global n_ataques_mitm_generados, n_ataques_replay_generados
    host = socket.gethostname()  # as both code is running on same pc
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 5005))
    text = ''
    for _ in range(mensajes_enviados):

        message = security.secureMessage(security.generaMensaje(), security.secretKey)
        r = random.random()
        ataque_mitm = r >= 0 and r < prob_mitm
        ataque_replay = r >= prob_mitm and r < (prob_mitm + prob_replay)
        
        stream_lock.acquire()
        #print('')
        stream_lock.release()
        if ataque_mitm:
            n_ataques_mitm_generados +=1
            message = security.mitm(message)
        
        s.send(message)  # send message
        data = s.recv(1024).decode()

        if ataque_replay:
            n_ataques_replay_generados +=1
            stream_lock.acquire()
            #print("\nREPLAY:")
            stream_lock.release()
            
            s.send(message)
            data = s.recv(1024).decode()
        

    s.close()# close the connection

t_server = threading.Thread(target=server_func).start()
t_client = threading.Thread(target=client_func).start()