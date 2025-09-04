from socket import * 

server_port = 10000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)

print("server is running.")

def host_string(hs:str) -> bool:
  if "Host: www.python.com\r\n" in hs:
    print("Host string True")
    return True
  
def request_line_end_check(end:str):
  print(end)
  if end == "HTTP/1\r\n" or end == "HTTP/1.1\r\n":
    print("end string True")
    return True
  else: 
    print("end string False")
    return False
  

def request_line(qry:str):
  qry = qry.split(' ')

  if qry[0] != 'GET':
    print("qry0 400 bad request resived")
    return
  
  if qry[1] == "/" or qry[1] == "/index.html":
    print("/index.html")
  elif qry[1] == "/test.html": 
    print("/test.html")
  else: 
    print("404 page not found")
    return
  
  if not request_line_end_check(qry[2]):
    print("400 bad request resived")
    return


while True:
  Connection_socket, addr = server_socket.accept()
  print(addr)
  message = Connection_socket.recv(2048)
  # to with request?

  http_request = message.decode().split('\n')
  for i in http_request:
    i = i + '\n'
    print(i)

  request_line(http_request[0])

  # server_response = "HTTP/1.1 200 OK\r\n"

  Connection_socket.send("hej\r\n".encode())
  Connection_socket.close()
