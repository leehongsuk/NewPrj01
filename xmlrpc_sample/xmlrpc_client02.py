import xmlrpc_sample.client
import datetime

proxy = xmlrpc_sample.client.ServerProxy("http://localhost:8000")

today = proxy.today()
converted = datetime.datetime.strptime(today.value, "%Y%m%dT%H:%M:%S" )
print(" Today is %s" % converted.strftime("%Y.%m.%d, %H:%M"))

