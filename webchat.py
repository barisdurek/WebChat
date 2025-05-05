import asyncio
import threading
import http.server
import socketserver
import websockets

# HTTP Server(runs in separate thread)
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/web.html"
        return super().do_GET()

def start_http_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"HTTP server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Websocket Server(runs in asyncio loop)
connected = set()

async def ws_handler(websocket):
    connected.add(websocket)
    try: # shares messages to all
        async for message in websocket:
            for conn in connected:
                await conn.send(message)
    except:
        pass
    finally:
        connected.remove(websocket)

async def start_ws_server():
    async with websockets.serve(lambda ws: ws_handler(ws), "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    # Start HTTP server in background thread
    threading.Thread(target=start_http_server, daemon=True).start()
    # Start WebSocket server in main asyncio loop
    asyncio.run(start_ws_server())