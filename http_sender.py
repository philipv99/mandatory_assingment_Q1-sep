from socket import * 

server_name = "127.0.0.1"
server_port = 10000

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

message = "GET /test.html HTTP/1.1\r\nHost: www.python.com\r\n\r\n"
client_socket.send(message.encode())

receive_message = client_socket.recv(2048)
print(receive_message.decode())

client_socket.close()