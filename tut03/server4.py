import select
import socket
import sys
import queue


inputs = []  
outputs = []  
message_queues = {}  
client_addresses = {}  


def create_socket():
    try:
        global host, port, server
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)  
    except socket.error as message:
        print("Socket Creation Error: " + str(message))
        exit(0)


def bind_socket():
    try:
        global host, port, server
        print("Binding the Port: " + str(port))
        server.bind((host, port))
        server.listen(0)
        inputs.append(server)
    except socket.error as message:
        print("Socket Binding Error: " + str(message))
        exit(0)


def echo(message):
    return message


def socket_accept(server):
    connection, address = server.accept()
    print("Connection has been established with " +
          address[0] + ":" + str(address[1]))
    client_addresses[connection] = address
    return connection


def generate_result(connection, data):
    address = client_addresses[connection]
    message = data.decode()  
    result = str(echo(message))
    print("Message received [" + message + "] from " +
          address[0] + ":" + str(address[1]))
    return result


def send_result(connection, result):
    address = client_addresses[connection]
    connection.send(result.encode())  
    print("Message sent to " + address[0] + ":" + str(address[1]))


def close_connection(connection):
    address = client_addresses[connection]
    connection.close()
    print("Connection has been closed with " +
          address[0] + ":" + str(address[1]))


def SELECT():
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)

        for s in readable:  
            if s is server:  
                connection = socket_accept(s)
                connection.setblocking(0)
                
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:  
                    result = generate_result(s, data)
                    message_queues[s].put(result)
                    if s not in outputs:
                        outputs.append(s)
                else:  
                    close_connection(s)
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del client_addresses[s]
                    del message_queues[s]

        for s in writable:
            try:
                next_message = message_queues[s].get_nowait()
            except queue.Empty:
                
                outputs.remove(s)
            else:
                send_result(s, next_message)

        for s in exceptional:  
            close_connection(s)
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            del client_addresses[s]
            del message_queues[s]


def main():
    create_socket()
    bind_socket()
    SELECT()


if __name__ == "__main__":
    
    main()
