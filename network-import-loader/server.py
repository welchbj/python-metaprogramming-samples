"""Module-providing server which support imports from client.py."""

import socketserver


class ModuleServer(socketserver.BaseRequestHandler):

    def handle(self):
        print('Handling connection...')
        with open('./hosted_module.py', 'rb') as f:
            self.request.sendall(f.read())


if __name__ == '__main__':
    host, port = '127.0.0.1', 12345
    with socketserver.TCPServer((host, port), ModuleServer) as server:
        server.serve_forever()
