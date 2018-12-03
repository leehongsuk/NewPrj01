# https://docs.python.org/3/library/xmlrpc.client.html
# Example of Client Usage

# simple test program (from the XML-RPC specification)
from xmlrpc.client import ServerProxy, Error

# server = ServerProxy("http://localhost:8000") # local server
with ServerProxy("http://localhost:8000") as proxy:
    print(proxy)

    try:
        print(proxy.add.getStateName(41))
    except Error as v:
        print("ERROR", v)
