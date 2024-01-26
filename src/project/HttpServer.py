from project.TcpServer import DEFAULT_PORT, LOCALHOST_ADDRESS, TCPServer
from project.constants import BLANK_LINE, HTTP_VERSION
from project.HTTPRequest import HTTPRequest
from project.HTTPStatus import HTTPStatus

import os
import json
import mimetypes


class HTTPServer(TCPServer):
    default_headers = {
        "Server": "Server",
        "Content-Type": "text/html",
    }

    def __init__(self):
        super().__init__()
        self.version = HTTP_VERSION

    def handle_request(self, data: bytes):
        """Handles the incoming request.
        Compiles and returns the response
        """

        request = HTTPRequest(data)

        try:
            handler = getattr(self, "handle_%s" % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response

    def handle_GET(self, request):
        filename = request.uri.strip("/")
        if filename == "":
            filename = "index.html"

        path = os.path.abspath("src/static/" + filename)

        if os.path.isfile(path):
            status = HTTPStatus.OK

            content_type = (
                mimetypes.guess_type(filename)[0]
                or self.default_headers["Content-Type"]
            )

            extra_headers = {"Content-Type": content_type}

            with open(path, "rb") as file:
                response_body = file.read()
        else:
            status = HTTPStatus.NOT_FOUND

            response_body = b"<h1>404 Not Found</h1>"

            extra_headers = {}

        return self._create_response(status, response_body, extra_headers)

    def handle_POST(self, request):
        status = HTTPStatus.CREATED

        json_file_path = "src/posts.json"

        # Load existing posts
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Append new post
        data["posts"].append(request.body)

        # Write back to file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file)

        return self._create_response(status=status)

    def HTTP_501_handler(self, request):
        response_body = b"<h1>501 Not Implemented</h1>"

        return self._create_response(HTTPStatus.NOT_IMPLEMENTED, response_body)

    def _response_line(self, status):
        """Returns response line"""

        line = "HTTP/%s %s %s\r\n" % (self.version, status, status.phrase)

        return line.encode()

    def _response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending
        extra headers for the current response
        """
        headers_copy = self.default_headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()

    def _create_response(self, status, body=b"", extra_headers=None):
        response_line = self._response_line(status)
        response_headers = self._response_headers(extra_headers)

        return b"".join([response_line, response_headers, BLANK_LINE, body])
