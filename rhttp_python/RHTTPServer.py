from typing import Optional, Dict, Tuple


class HTTPRequest:
    def __init__(self, method: str, path: str, headers: Dict[str, str], query: Optional[Dict[str, str]] = None,
                 body: Optional[str] = None):
        self.method = method
        self.path = path
        self.headers = headers
        self.query = query
        self.body = body

    def to_string(self) -> str:
        query_str = ""
        if self.query:
            query_list = [f"{k}={v}" for k, v in self.query.items()]
            query_str = "?" + "&".join(query_list)

        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])

        return f"{self.method} {self.path}{query_str} HTTP/1.1\r\n{headers_str}\r\n\r\n{self.body}" if self.body else f"{self.method} {self.path}{query_str} HTTP/1.1\r\n{headers_str}\r\n"


class HTTPResponse:
    def __init__(self, status_code: int, status_message: str, headers: Dict[str, str], body: Optional[str] = None):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body

    def to_string(self) -> str:
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])

        return f"HTTP/1.1 {self.status_code} {self.status_message}\r\n{headers_str}\r\n\r\n{self.body}" if self.body else f"HTTP/1.1 {self.status_code} {self.status_message}\r\n{headers_str}\r\n"


def parse_http_string(http_string: str) -> Tuple[HTTPRequest, HTTPResponse]:
    lines = http_string.split("\r\n")
    request_line, *header_lines, body = lines

    # Parse the request or response line
    if request_line.startswith("HTTP"):
        _, status_code, status_message = request_line.split(" ")
        response = True
    else:
        method, path, _ = request_line.split(" ")
        response = False

    headers = {k: v for k, v in (line.split(": ") for line in header_lines) if k}
    body = body.strip() if body else None

    # Construct the appropriate object and return it
    if response:
        return None, HTTPResponse(int(status_code), status_message, headers, body)
    else:
        path, *query = path.split("?")
        query = {k: v for k, v in (item.split("=") for item in query)} if query else None
        return HTTPRequest(method, path, headers, query, body), None


def stringify_http_object(http_object) -> str:
    if isinstance(http_object, HTTPRequest) or isinstance(http_object, HTTPResponse):
        return http_object.to_string()
    else:
        raise TypeError("Invalid HTTP object")


class RHTTPServer:
    ...
