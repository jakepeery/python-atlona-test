

import socket
from datetime import datetime
from datetime import timedelta

pollTime = 5    #time in seconds to poll switcher
timeout = .5


def MakeRequest():
    host = "127.0.0.1"
    port = 5000  # socket server port number
    
    sock = socket.socket()  # instantiate
    sock.settimeout(timeout)
    
    try:
        sock.connect((host, port))  # connect to the server
    except Exception as err:
        output = "ERROR: " + str(err)
        WriteLog(output)


    try:
        data = sock.recv(1024).decode()  # receive initialresponse
        output = "Initial Response: " + data
        WriteLog(output)
    except Exception as err:
        output = "ERROR: " + str(err)
        WriteLog(output)

    
    try:
        message = "Status\r"
        sock.send(message.encode())  # send message
        output = "Send Message: " + message
        WriteLog(output)
    except Exception as err:
        output = "ERROR: " + str(err)
        WriteLog(output)
    
    try:
        data = sock.recv(1024).decode()  # receive initialresponse
        output = "Message Response: " + data
        WriteLog(output)
    except Exception as err:
        output = "ERROR: " + str(err)
        WriteLog(output)

    sock.close()  # close the connection
    
    #verify socket is closed by trying to write to it
    try:
        message = "Should be closed\r"
        sock.send(message.encode())  # send message
        output = "Send Message: " + message
        WriteLog(output)
    except Exception as err:
        output = "Socket should be closed: " + str(err)
        WriteLog(output)

def WriteLog(info):
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S.%f")
    output = "{t}: {i}\r".format(t=currentTime, i=info)
    print(output)
    f = open("log.txt", "a")
    f.write(output)
    f.close()
    
count = 0
if __name__ == '__main__':
    nextTrigger = datetime.now()
    while True:
        currentTime = datetime.now()
        if currentTime > nextTrigger:
            nextTrigger = currentTime + timedelta(seconds=pollTime)
            WriteLog("\r\nNew Request #" + str(count))
            MakeRequest()
            count += 1
        
    
   