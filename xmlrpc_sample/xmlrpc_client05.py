# https://docs.python.org/3/library/xmlrpc.client.html
# ProtocolError Objects
import xmlrpc.client


proxy = xmlrpc.client.ServerProxy("http://google.com")

try:
    proxy.some_method()
except xmlrpc.client.ProtocolError as err:
    print("A protocol Error occurred")
    print("URL : %s" % err.url)
    print("HTTP/HTTPS Headers : : %s" % err.headers)
    print("Error code : %d" % err.errcode)
    print("Error Message  : %s" % err.errmsg)







