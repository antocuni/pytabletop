import sys
import requests

def reveal():
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


def show_image():
    url = 'http://127.0.0.1:5000/show_image/'
    files = {'image': open(sys.argv[1],'rb')}
    resp = requests.post(url, files=files)
    print resp
    print resp.text


show_image()
