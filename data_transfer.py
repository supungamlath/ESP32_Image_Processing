import json
import urllib.request


def send_control_packet(url, data):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url + '/post', data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
        return response.read().decode('utf-8')
