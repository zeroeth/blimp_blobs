import socket
import time

def connect(ip,port):
    #make a client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #keep trying to connect to the server until success
    print("connecting to control server...")
    connected = False
    while not connected:
        try:
            s.connect((ip, port))
            connected = True
        except Exception as err:
            pass
    print("connected")
    return s

def getPosition():
    #compute it, or grab it from wherever it's store
    return 1.0, 1.0, 1.0

def main():
    ip = "127.0.0.1"
    port = 7779
    size = 1024
    
    #first get a connection to the server
    s = connect(ip,port)

    #now just spin on the stream writing a position
    while 1:
        try:
            x,y,z = getPosition()
            msg = "" + `x` + "," + `y` + "," + `z` + "\n"
            s.send(msg)
            time.sleep(1)
        except Exception as err:
            print("disconnected")
            #we got disconnected somehow, reconnect
            s = connect(ip,port)

    s.close()

        
if __name__ == "__main__":
    main()
