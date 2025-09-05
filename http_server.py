from socket import * 
import time
import os

server_port = 10000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)

RESPONSE_CODES = {200: "200 OK", 400: "400 bad request", 404: "404 not found"}
HTTP_VERSIONS = ["HTTP/1", "HTTP/1.1"]
ALLOWED_PATHS = ["index.html", "test.html"]


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
def http_get_rel_path(path:str) -> str|None:
  
    if path == "/" : "/index.html"


    cleaned = os.path.normpath(path.lstrip("/"))
    if cleaned.startswith(".."):
        return None
    return cleaned
  




def read_until_double_crlf(conn: socket) -> bytes:
    """Read headers until CRLFCRLF. Simple and good enough for small requests."""
    data = b""
    #print(data)
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > 65536:  # defensive: 64 KB header cap
            break
    return data

RESPONSE_PHRASES = {
    200: "OK",
    400: "Bad Request",
    404: "Not Found",
}

@log_function_call
def server_HTTP_response(status: int, body, headers: dict | None = None):
    #print("1")
    reason = RESPONSE_PHRASES.get(status, "Unknown")
    lines = [f"HTTP/1.1 {status} {reason}"]
    
    base_headers = {
        "Date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
        "Server": "TinyPy/0.1",
        "Content-Length": str(len(body)),
        "Connection": "close",
    }
    if headers:
        base_headers.update(headers)
    for k, v in base_headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")  # end of headers
    lines.append("")  # header/body separator => adds the required extra CRLF
    head = "\r\n".join(lines).encode("iso-8859-1", errors="replace")

    #print(head)
    #print(body)
    return head + body



#server stat
action_logging("server is started.")
while True:
    Connection_socket, addr = server_socket.accept()
    action_logging(f"connected: [{addr}]")

    try:
        raw = read_until_double_crlf(Connection_socket)
        action_logging(f"message resived: {raw.decode().strip()}")
        header_text = raw.split(b"\r\n\r\n", 1)[0].decode()
        lines = header_text.split("\r\n")

        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) != 3:
            Connection_socket.sendall(server_HTTP_response(400, b""))
        method, path, version = parts



        if method != "GET":
            # We only support GET in this tiny server
            body = b"Only GET supported."
            Connection_socket.sendall(server_HTTP_response(400))
            

        headers = {}
        for h in lines[1:]:
            if ":" in h:
                k, v = h.split(":", 1)

                headers[k.strip().lower()] = v.strip()

        rel_path = http_get_rel_path(path)
        if rel_path not in ALLOWED_PATHS:
            Connection_socket.sendall(server_HTTP_response(404, b""))

        with open(rel_path, "rb") as f:
            body = f.read()
        
                
        resp = server_HTTP_response(200, body, {"Content-Type": "text/html"})

        Connection_socket.sendall(resp)
        
        if resp:
            """  http_get_request = http_request_line_check(http_request)
            http_request_data = http_get_rel_path(http_get_request)
        send_response_to_client(server_HTTP_response(200, http_request_data.lenght())) """

        action_logging(f"message resived: {raw.decode().strip()}")
    except Exception as e:
        action_logging(f"server sendt: {e}")
        #send_response_to_client(server_HTTP_response(400))
    finally:
        Connection_socket.shutdown(SHUT_WR)
        action_logging(f"{addr} connection closed")

