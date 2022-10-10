import socket
import threading
import socket
import security

stream_lock = threading.Lock()

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
        # Getting printing stream lock is important
        stream_lock.acquire()
        print("Received:", str(data))
        if True:
            print("Transaction Accepted")
            conn.send("OK".encode())
        else:
            print("Transaction Denied")
            conn.send("FAILED".encode())
        stream_lock.release()
        
    conn.close()

def client_func():
    host = socket.gethostname()  # as both code is running on same pc
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 5005))
    text = ''
    while text.lower().strip() != 'bye':
        stream_lock.acquire()
        text = input(" > ")  # again take input 
        message = security.secureMessage(text, security.secretKey)
        stream_lock.release()
        s.send(message)  # send message
        data = s.recv(1024).decode()
           
    s.close()# close the connection

t_server = threading.Thread(target=server_func).start()
t_client = threading.Thread(target=client_func).start()