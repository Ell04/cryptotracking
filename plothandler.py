import os
import http.server
import socketserver
import webbrowser
import threading
import time


PORT = 8000
DIRECTORY = os.path.join(os.getcwd(), "plots")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def run_server_with_browser():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    time.sleep(1.5)  # wait for server to start

    webbrowser.open(f"http://localhost:{PORT}/index.html")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped by user")

if __name__ == "__main__":
    run_server_with_browser()