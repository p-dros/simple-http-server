from project.HttpServer import HTTPServer
from project.HTTPStatus import HTTPStatus


def main():
    server = HTTPServer()
    server.start()


if __name__ == "__main__":
    main()
