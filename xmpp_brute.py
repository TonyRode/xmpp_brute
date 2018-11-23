import socket
import threading


mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mysock.bind(('127.0.0.1', 65535))

mysock.listen(1)

conns = []

def handler(c, a):
    global conns
    while True:
        data = c.recv(1500)
        # Treat data here
        print (data)
        if not data:
            conns.remove(c)
            c.close()
            break
                    
while True:
    c, a = mysock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.daemon = True
    cThread.start()
    conns.append(c)
