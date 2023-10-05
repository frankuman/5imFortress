from gevent import socket
from conpot.protocols.http import web_server
import requests
 
def test_do_POST():
        """
        Objective: send a POST request to a invalid URI. Should get a 404 response
        """
        payload = {'key1': 'value1', 'key2': 'value2'}
        ret = requests.post("http://127.0.0.1:80", data=payload)


test_do_POST()