import os, http.server, socketserver
port = int(os.environ.get("PORT", "8765"))
with socketserver.TCPServer(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as s:
    print(f"serving on {port}")
    s.serve_forever()
