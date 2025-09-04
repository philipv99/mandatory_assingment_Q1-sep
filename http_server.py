from socket import * 

server_port = 10000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)

RESPONSE_CODES = {200: "200 OK", 400: "400 bad request", 404: "404 not found"}

print("server is running.")

def host_string(hs:str) -> bool:
  if "Host: www.python.com\r\n" in hs:
    print("Hostname: Approved")
    return True
  else:
    print("Hostname: Approved")
    return False
  
  
def request_line_end_check(end:str):
  if end == "HTTP/1\r\n" or end == "HTTP/1.1\r\n":
    return True
  else: 
    return False
  

def request_line(qry:str):
  qry = qry.split(' ')
  file_to_send = ""

  if qry[0] != 'GET':
    return RESPONSE_CODES[400]

  if not request_line_end_check(qry[2]):
    return RESPONSE_CODES[400]
  
  return fill_operation(qry[1])
  
  
def fill_operation(qry:str):
  fill_qry = qry
  if qry == '/':
    fill_qry = "/index.html"
  try:
    file_object = open(fill_qry.removeprefix('/'), "r")
    response_data = file_object.read()
    file_object.close()
    return server_HTTP_response(200, response_data)
  except:
    print(RESPONSE_CODES[404])
    return RESPONSE_CODES[404]


def server_HTTP_response(code:int, data:str=None) -> str:
  prefix = "HTTP/1.1 "
  affix = "\r\n"
  re = prefix + RESPONSE_CODES[code] + affix
  if data is not None:
    re = re + data + "\r\n\r\n"
  return re


#server stat
while True:
  Connection_socket, addr = server_socket.accept()
  server_response = ""
  print(addr)
  message = Connection_socket.recv(2048)
  # to with request?

  http_request = message.decode().split('\n')
  for i, v in enumerate(http_request):
    http_request[i] = http_request[i] + '\n'
  http_request.pop(3)

  
  if host_string(http_request[1]) and http_request[2] == '\r\n':
    server_response = request_line(http_request[0])
  print(server_response)

  Connection_socket.send(server_response.encode())
  Connection_socket.close()
