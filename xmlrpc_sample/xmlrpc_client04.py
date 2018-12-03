# https://docs.python.org/3/library/xmlrpc.client.html
# Fault Objects
import xmlrpc.client


proxy = xmlrpc,client.ServerProxy("http://localhost:8000")
try:
    proxy.add(2, 5)
except xmlrpc.client.Fault as err:
    print("A Fault occured")
    print("Fault code %d", err.faultCode)
    print("Fault string %s", err.faultString)


