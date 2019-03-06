import requests

url = 'http://127.0.0.1:5000/reveal/'

payload = {
    'areas': [
        {'type': 'rectangle', 'pos': [200, 0], 'size': [110, 110]},
        {'type': 'rectangle', 'pos': [400, 400], 'size': [200, 200]},
        ]
    }

resp = requests.post(url, json=payload)
print resp
print resp.text

