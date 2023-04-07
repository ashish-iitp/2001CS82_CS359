import socket
import sys

clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]  
port = int(sys.argv[2])

try:
    clt.connect((host, port))
    clt.close()
    c.connect((host, port))  
    print("Successfully connected to the server.")
except socket.error as message:
    print("Error: Cannot connect to socket" + str(message))
    exit(0)

while True:  
    inp = input("Enter the message : ")
    c.send(inp.encode())
    answer = c.recv(1024)
    print("Server response : " + answer.decode())
    inp = input("Do you move forward ? Y/N\n")
    if (inp == "N"):
        break

c.close()
