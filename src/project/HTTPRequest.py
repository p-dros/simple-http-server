from project.constants import HTTP_VERSION


class HTTPRequest:
    def __init__(self, data: bytes):
        self.method = None
        self.uri = None
        self.http_version = "HTTP/1.1"
        self.headers = {}

        self.parse(data)

    def parse(self, data: bytes):
        data = data.decode()
        req_lines = data.split("\r\n\r\n")

        request_line_and_headers = req_lines[0].split("\r\n")
        request_line = request_line_and_headers[0]
        self._parse_request_line(request_line)

        header_lines = request_line_and_headers[1:]
        self._parse_headers(header_lines)

        if len(req_lines) > 1:
            self.body = req_lines[1]
        else:
            self.body = None

    def _parse_headers(self, header_lines: list[str]):
        self.headers = {}

        for line in header_lines:
            if line:
                key, value = line.split(":", 1)
                self.headers[key.strip()] = value.strip()

    def _parse_request_line(self, request_line):
        self.method, self.uri, self.http_version = request_line.split(" ")
