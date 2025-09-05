from socket import * 
import time

server_port = 10000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)

RESPONSE_CODES = {200: "200 OK", 400: "400 bad request", 404: "404 not found"}
HTTP_VERSIONS = ["HTTP/1", "HTTP/1.1"]

# logging
def action_logging(input):
  logging(f"[{time.ctime()}]")
  logging(input)
  logging("\n")
  print(f"[{time.ctime()}]")
  print(input)

def logging(input):
  with open("log.txt", "a") as log:
    log.write(str(input) + '\n')

def log_function_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging(f"[{time.ctime()}]")
        logging(f"Calling function: {func.__name__} with arguments: {args} and keyword arguments: {kwargs}")
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging(f"Function: {func.__name__} (Execution time: {execution_time:.4f} seconds)")
        logging("\n")
        return result
    return wrapper

@log_function_call
def http_host_acceptet(hs:str) -> bool:
  if "Host: www.python.com\r\n" in hs:
    return True
  else:
    print("Hostname: denied")
    return False
  

@log_function_call  
def send_response_to_client(response:str) -> None:
  action_logging(f"server responded: {response}")
  Connection_socket.send(response.encode())
  Connection_socket.close()
  action_logging("connection closed")

@log_function_call
def http_request_line_check(qry:str) -> list:
  get, path, version = qry.split(' ') #split http -> 0:[get] 1:[/...] 2:[http/1.1\r\n]
  if get != 'GET':
    send_response_to_client(server_HTTP_response(400, "operation not autoherised"))
  if version in HTTP_VERSIONS:
    send_response_to_client(server_HTTP_response(400, "version not supported"))
  return path
  
@log_function_call
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

@log_function_call
def server_HTTP_response(code:int, data:str=None) -> str:
  prefix = "HTTP/1.1 "
  affix = "\r\n"
  re = prefix + RESPONSE_CODES[code] + affix
  if data is not None:
    re = re + data + "\r\n\r\n"
  return re

#server stat
action_logging("server is started.")
while True:
  Connection_socket, addr = server_socket.accept()
  action_logging(f"connected: [{addr}]")
  message = Connection_socket.recv(2048)
  action_logging(f"message resived: {message.decode().strip()}")

  try:
    http_request, http_host, http_request_newline, line = message.decode().split('\n')
    http_request, http_host, http_request_newline = http_request + '\n', http_host + '\n', http_request_newline + '\n'
    if http_host_acceptet(http_host) and http_request_newline == '\r\n':
      http_get_request = http_request_line_check(http_request)
      http_request_data = http_request_fill_retrive(http_get_request)
    send_response_to_client(server_HTTP_response(200, http_request_data))
  except:
    action_logging(f"server sendt: {server_HTTP_response(400)}")
    send_response_to_client(server_HTTP_response(400))
  finally:
    action_logging(f"{addr} connection closed")
    
