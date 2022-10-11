import socket
import threading
import socket
import security
import pathlib
import os

stream_lock = threading.Lock()

#Configuración de la gestión del Log
script_path = pathlib.Path(__file__).parent.parent.resolve()
register_filename = "registro.log"
register_path = os.path.join(script_path, register_filename)

registro= open(register_path, "w", encoding="utf-8")

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
        mensaje_cliente = data[:16].decode()
        mensaje_con_nonce = data[:-32]
        nonce = mensaje_con_nonce[-20:].decode()
        print(nonce)
        macDigest = data[-32:]
        # Getting printing stream lock is important
        stream_lock.acquire()
        print("Received:", mensaje_cliente)
        mensaje = security.random_Mitm(mensaje_cliente,nonce)
        if security.nonceHaSidoUsado(nonce):    
            print("Transaction Denied: Nonce ya usado (Ataque Replay)")
            security.write_to_log(registro,"Ataque Replay","Mensaje:"+mensaje)
            conn.send("FAILED".encode())
        elif security.check_man_in_the_middle(mensaje.encode(), macDigest):
            print("Transaction Denied: Mac distinta Cliente/Servidor (Ataque MITM)")
            security.write_to_log(registro,"Ataque MITM","Mensaje:"+mensaje[:17])
            conn.send("FAILED".encode())
        else:
            print("Transaction Accepted")
            security.agregaNonceAlRegistro(nonce)
            conn.send("OK".encode())
        stream_lock.release()
        
    conn.close()

def client_func():
    host = socket.gethostname()  # as both code is running on same pc
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 5005))
    text = ''
    for _ in range(100):
        #stream_lock.acquire()
        #text = input(" > ")  # again take input 
        message = security.secureMessage(security.generaMensaje(), security.secretKey)
        #stream_lock.release()
        s.send(message)  # send message
        data = s.recv(1024).decode()
           
    s.close()# close the connection

t_server = threading.Thread(target=server_func).start()
t_client = threading.Thread(target=client_func).start()