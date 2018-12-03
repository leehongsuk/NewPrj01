# https://docs.python.org/3/library/xmlrpc.client.html
# Example of Client Usage

# simple test program (from the XML-RPC specification)
from xmlrpc.client import ServerProxy, Error

# 이 프로그램을 실행하면, 원격 서버에 연결하여 미국의 주명(state name)을 얻어 출력한다. (이 예제에서 41번 주는 South Dakota 일 것이다.)
# https://wiki.kldp.org/HOWTO/html/XML-RPC-HOWTO/xmlrpc-howto-intro.html
# server = ServerProxy("http://localhost:8000") # local server
with ServerProxy("http://betty.userland.com/RPC2") as proxy:
    print(proxy)

    try:
            print(proxy.examples.getStateName(41))
    except Error as v:
        print("ERROR", v)


