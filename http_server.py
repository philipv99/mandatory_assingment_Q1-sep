from socket import * 

server_port = 10000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)

RESPONSE_CODES = {200: "200 OK", 400: "400 bad request", 404: "404 not found"}
HTTP_VERSIONS = ["HTTP/1", "HTTP/1.1"]

print("server is running.")

def http_host_acceptet(hs:str) -> bool:
  if "Host: www.python.com\r\n" in hs:
    return True
  else:
    print("Hostname: denied")
    return False
  
def send_response_to_client(response:str) -> None:
  Connection_socket.send(response.encode())
  Connection_socket.close()

def http_request_line_check(qry:str) -> list:
  get, path, version = qry.split(' ') #split http -> 0:[get] 1:[/...] 2:[http/1.1\r\n]
  if get != 'GET':
    send_response_to_client(server_HTTP_response(400, "operation not autoherised"))
  if version in HTTP_VERSIONS:
    send_response_to_client(server_HTTP_response(400, "version not supported"))
  return path
  
  
def http_request_fill_retrive(path:str) -> str|None:
  path = path if path != '/' else "/index.html"
  try:
    file_object = open(path.removeprefix('/'), "r")
    response_data = file_object.read()
    file_object.close()
  except:
    send_response_to_client(server_HTTP_response(404))
    return
  return response_data


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
  message = Connection_socket.recv(2048)
  print(addr, "connected")

  try:
    http_request, http_host, http_request_newline, line = message.decode().split('\n')
    http_request, http_host, http_request_newline = http_request + '\n', http_host + '\n', http_request_newline + '\n'
    if http_host_acceptet(http_host) and http_request_newline == '\r\n':
      http_get_request = http_request_line_check(http_request)
      http_request_data = http_request_fill_retrive(http_get_request)
    send_response_to_client(server_HTTP_response(200, http_request_data))
  except: 
    send_response_to_client(server_HTTP_response(400))
    print("400 response send")
  finally:
    print(addr, "connection closed")
    
