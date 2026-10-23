#!/usr/bin/env python3
"""
Medchanic.MD — Workspace File Hub
Serves the workspace so every file opens in its FINAL view (rendered HTML,
PDF viewer, images) with a download button on every file.

  Run:  python3 server.py     (port 8000, binds 0.0.0.0)

Routes:
  /               -> files.html   (the hub page: view + download buttons)
  /__list.json    -> JSON listing of every workspace file (for the hub)
  anything else   -> the file itself, correct MIME, no-cache
"""
import http.server
import json
import os
import socketserver
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8000


class Hub(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    # -- silence default stderr noise per request, keep errors visible
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        # the hub itself
        if path == "/":
            self.path = "/files.html"
            return super().do_GET()

        # JSON file listing for the hub page
        if path == "/__list.json":
            files = []
            for dirpath, dirnames, filenames in os.walk(ROOT):
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                for fn in filenames:
                    full = os.path.join(dirpath, fn)
                    rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                    try:
                        size = os.path.getsize(full)
                    except OSError:
                        continue
                    files.append({"path": rel, "size": size})
            files.sort(key=lambda f: f["path"].lower())
            body = json.dumps(files).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Hub) as httpd:
        print(f"File hub running → http://0.0.0.0:{PORT}  (serving {ROOT})")
        httpd.serve_forever()
