from ..sockets.server.tcplistener import TcpListener
from .httpclientmodel import HttpClientModel
from .httprequest import HttpRequest

from jinja2 import Environment, FileSystemLoader

class WebServerAttributes:
    def __init__(self, contextRoute, errorFile):
        self.contextRoute = contextRoute
        self.errorFile = errorFile

        self.actions = {}

        self.jinja_env = Environment(loader=FileSystemLoader(self.contextRoute))

class HttpServer(TcpListener):
    def __init__(self, ipAddr, port):
        super().__init__(ipAddr, port, 512, True, True)

        self.atts = WebServerAttributes("content", "error.html")

    def cmdThread(self):
        cmd = ""

        while True:
            cmd = input()
            if cmd == "stop":
                break

    def clientThread(self, client):
        while True:
            data = client.sock.recv(1024).decode("latin1")

            if data:
                self.msgReceived(client, data)
                data = None

        self.clientDisconnected(client)
        client.sock.close()
        self.client.remove(client)

    def generateClientObject(self, clientsock, clientaddr):
        return HttpClientModel(clientsock, clientaddr)

    def serverStarted(self):
        print(f"HTTP Server started at {self.ipAddr}:{self.port}")

    def clientConnected(self, client):
        pass

    def clientDisconnected(self, client):
        pass

    def msgReceived(self, client, msg):
        req = HttpRequest(client, msg, self.atts)
        req.parse()
        req.follow()

        self.send(client, req.genResponse(), not req.bytes, False)

    def addApp(self, app):
        self.atts.actions.update(app.getRoutes())