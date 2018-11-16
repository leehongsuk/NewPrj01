import datetime
from xmlrpc_sample.server import SimpleXMLRPCServer
import xmlrpc_sample.client


def today():
    today1 = datetime.datetime.today()
    return xmlrpc_sample.client.DateTime(today1)


server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000")
server.register_function(today, "today")
server.serve_forever()

