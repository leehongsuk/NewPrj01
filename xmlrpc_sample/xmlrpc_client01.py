import xmlrpc_sample.client

with xmlrpc_sample.client.ServerProxy("http://localhost:8000") as proxy:
    print("3 is even : %s" % str(proxy.is_even(3)))
    print("100 is even : %s" % str(proxy.is_even(100)))
