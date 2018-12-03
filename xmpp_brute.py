import socket
import threading


with open("config") as f:
    content = f.readlines()
content = [x.strip() for x in content]


mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mysock.bind(('127.0.0.1', 65535))

mysock.listen(1)

def handler(c, a):
    i = 0
    try:
        while True:
            data = c.recv(1500)
            #print ("request " + str(i) + " data : " + data.hex())
            # as hydra bypasses the 1rst request after the 1rst iteration, we check if we receive the 2nd packet, if so we jump to the 2nd step and continue.
            # change this according if not SCRAM SHA1 used
            if (data.hex() == "3c6175746820786d6c6e733d2775726e3a696574663a706172616d733a786d6c3a6e733a786d70702d7361736c27206d656368616e69736d3d27534352414d2d5348412d31272f3e"):
                i = 1
            if (i == 0):
                # sends SCRAM-SHA1 allowed mechanism (force it), or whatever is defined in the config file
                c.send(bytes.fromhex(content[0]))
            if (i == 1):
                # sends empty challenge
                c.send(bytes.fromhex("3c6368616c6c656e676520786d6c6e733d2775726e3a696574663a706172616d733a786d6c3a6e733a786d70702d7361736c273e3c2f6368616c6c656e67653e"))
            if (i == 2):
                # sends real challenge (in case of succeed)
                c.send(bytes.fromhex(content[1]))
            if (i == 3):
                # if good password was used
                if (data.hex() == content[2]):
                    c.send(bytes.fromhex(content[3]))
                    print ("Found !!! -> Have a look at Hydra !")
                else:
                    # sends failure
                    c.send(bytes.fromhex("3c6661696c75726520786d6c6e733d2775726e3a696574663a706172616d733a786d6c3a6e733a786d70702d7361736c273e3c696e76616c69642d617574687a69642f3e3c2f6661696c7572653e"))
                #print (data)
            i = (i + 1) % 4
            if not data:
                c.close()
                break
    except:
        c.close()
            
while True:
    c, a = mysock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.daemon = True
    cThread.start()
