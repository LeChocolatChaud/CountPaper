from http.server import ThreadingHTTPServer
from server import WebHandler, APIHandler
from threading import Thread

web_server = ThreadingHTTPServer(('localhost', 8000), WebHandler)
api_server = ThreadingHTTPServer(('localhost', 8001), APIHandler)

def run_web_server():
    global web_server
    web_server.serve_forever()

def run_api_server():
    global api_server
    api_server.serve_forever()

if __name__ == "__main__":
    web_server_thread = Thread(target=run_web_server)       # multi threading to run multiple server at once
    api_server_thread = Thread(target=run_api_server)
    web_server_thread.start()
    api_server_thread.start()
    print("Server started")
    input()                         # a janky way to stop the server
    print("Server stopped")
    web_server.shutdown()
    api_server.shutdown()
