import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
with open("./images/python_logo_write.jpg", "wb") as handle:
    handle.write(proxy.python_logo().data)
