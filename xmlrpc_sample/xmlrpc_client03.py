# https://docs.python.org/3/library/xmlrpc.client.html
# Binary Objects
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
with open("./images/python_logo_write.jpg", "wb") as handle:
    handle.write(proxy.python_logo().data)
