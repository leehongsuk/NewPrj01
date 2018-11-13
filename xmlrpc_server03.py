from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client


def python_logo():
    with open("./images/python_logo.jpg", "rb") as handle:
        return xmlrpc.client.Binary(handle.read())


server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port  8000...")
server.register_function(python_logo, "python_logo")

server.serve_forever()
