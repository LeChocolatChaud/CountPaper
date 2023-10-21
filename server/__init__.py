#!/usr/bin/env python
# coding: utf-8

import cv2
from sys import argv

import numpy as np
import math

def do_count(filebytes):
    # 读取图片
    nparr = np.fromstring(filebytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = img[0: img.shape[0] // 3, 0: img.shape[1]]
    cv2.imwrite('cropped.jpg', img)

    # Canny算法
    edges = cv2.Canny(img,100,200) # 第二个参数和第三个参数分别是低阈值和高阈值
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)  #连通区域分析（一个连通区域表示一个线条）
    lines = []
    print(contours[0])
    for contour in contours:
        X = [i[0][0] for i in contour]
        Y = [i[0][1] for i in contour]
        z1 = np.polyfit(X, Y, 1)
        if abs(z1[0]) < 10:
            continue
        x = contour[0][0][0]
        y = contour[0][0][1]
        if abs(z1[0] * x - y + z1[1]) / math.sqrt(z1[0] ** 2 + 1) < 1.26:
            continue
        lines.append(z1)
    return len(lines)


from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
import base64

class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)

class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        with open('out.txt', 'w') as f:
            f.write(body.decode('utf-8'))
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
