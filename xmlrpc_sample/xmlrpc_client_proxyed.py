# https://docs.python.org/3/library/xmlrpc.client.html
# Example of Client Usage

import http.client
import xmlrpc.client


class ProxyedTransport(xmlrpc.client.Transport):

    def set_proxy(self, host, port=None, headers=None):
        self.proxy = host, port
        self.proxy_headers = headers

   def make_connection(self, host):
       connection = http.client.HTTPConnection(*self.proxy)
       connection.set_tunnel(host, headers=self.proxy_headers)
       self._connection = host, connection
       return connection

transport = ProxyedTransport()
transport.set_proxy("proxt-server", 8080)
server = xmlrpc.client.ServerProxy("http://betty.yourland,com", transport=transport)
print(server.examples.getStateName(41))