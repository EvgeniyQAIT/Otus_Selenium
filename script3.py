import socket
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 5000

def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server running on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                request = "".join((line + "\n") for line in data.splitlines())
                request_head, request_body = request.split("\n\n", 1)
                request_head = request_head.splitlines()
                request_headline = request_head[0]
                request_headers = dict(x.split(": ", 1) for x in request_head[1:] if ":" in x)
                request_method, request_uri, request_proto = request_headline.split(" ", 2)
                parsed_url = urlparse(request_uri)
                captured_value = parse_qs(parsed_url.query)
                status_code = HTTPStatus.OK
                http_status_name = status_code.name
                try:
                    if "status" in captured_value:
                        status_code = HTTPStatus(int(captured_value["status"][0]))
                        http_status_name = status_code.name
                except Exception as e:
                    print(f"Invalid status code: {e}")
                    status_code = HTTPStatus.OK
                    http_status_name = status_code.name

                request_ip, request_port = request_headers.get("Host", "127.0.0.1:5000").split(":", 1)
                response_body = [
                    f"Request Method: {request_method}",
                    f"Request Source: ('{request_ip}', {int(request_port)})",
                    f"Response Status: {status_code.value} {http_status_name}"
                ]
                for request_header_name, request_header_value in request_headers.items():
                    response_body.append(f"{request_header_name}: {request_header_value}")
                response_body_raw = "\r\n".join(response_body)
                response_proto = "HTTP/1.1"
                response_status = status_code.value
                response_status_text = http_status_name

                conn.sendall(
                    f"{response_proto} {response_status} {response_status_text}\r\n".encode('utf-8')
                )
                response_headers = {
                    "Content-Type": "text/plain; charset=utf-8",
                    "Content-Length": len(response_body_raw),
                    "Connection": "close"
                }

                response_headers_raw = "".join(
                    f"{k}: {v}\r\n" for k, v in response_headers.items()
                )
                conn.sendall(response_headers_raw.encode('utf-8') + b"\r\n" + response_body_raw.encode('utf-8'))

run_server(HOST, PORT)
