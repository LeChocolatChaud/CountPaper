# opencv part

import cv2
from sys import argv

import numpy as np
import math

def do_count(filebytes):
    # read the image
    nparr = np.fromstring(filebytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = img[0: img.shape[0] // 3, 0: img.shape[1]]       # crop the image for better samples

    # Canny algorithm
    edges = cv2.Canny(img,100,200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # analyze contours
    lines = [] # results
    for contour in contours:            # rule out unwanted and duplicated contours
        X = [i[0][0] for i in contour]
        Y = [i[0][1] for i in contour]
        z1 = np.polyfit(X, Y, 1)
        if abs(z1[0]) < 10:             # not steep enough
            continue
        x = contour[0][0][0]
        y = contour[0][0][1]
        if abs(z1[0] * x - y + z1[1]) / math.sqrt(z1[0] ** 2 + 1) < 1.26:   # detect duplications, needs a bit more adjusting...
            continue
        lines.append(z1)
    return len(lines)

# server part

from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
import base64

class WebHandler(SimpleHTTPRequestHandler):         # web interface
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)

class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body = json.loads(body.decode("utf-8"))
        match (self.path):
            case "/count":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                image = body["image"]
                print(image)
                if "jpeg" in image or "jpg" in image:
                    data = image.split(";")[1][7:]
                    count = do_count(base64.b64decode(data))
                    self.wfile.write(json.dumps({"count": count}).encode())
            case _:
                self.send_response(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
