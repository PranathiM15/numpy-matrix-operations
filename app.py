"""A small NumPy matrix operations web app built with Python's standard library."""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from matrix_ops import calculate

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}


class MatrixHandler(BaseHTTPRequestHandler):
    server_version = "MatrixStudio/1.0"

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(200, {"status": "ok", "service": "NumPy Matrix Studio"})
            return
        if path in ("/", "/index.html"):
            self._send_file(STATIC / "index.html")
            return
        if path in ("/styles.css", "/app.js"):
            self._send_file(STATIC / path.lstrip("/"))
            return
        self._send_json(404, {"error": "Page not found."})

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if urlparse(self.path).path != "/api/compute":
            self._send_json(404, {"error": "Endpoint not found."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100_000:
                raise ValueError("Send a request body smaller than 100 KB.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("The request must be a JSON object.")
            result = calculate(payload.get("matrix_a"), payload.get("matrix_b"), payload.get("operation"))
            self._send_json(200, result)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON."})
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception:
            # Avoid leaking stack traces or implementation details to browser clients.
            self._send_json(500, {"error": "An unexpected error occurred. Please try again."})

    def _send_file(self, path: Path) -> None:
        if not path.is_file() or path.parent != STATIC:
            self._send_json(404, {"error": "File not found."})
            return
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", MIME_TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, status: int, data: dict) -> None:
        content = json.dumps(data, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string: str, *args: object) -> None:
        # Keep console logs compact while still showing request activity.
        print(f"[{self.log_date_time_string()}] {format_string % args}")


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    # Hosting platforms route public traffic to services bound to 0.0.0.0.
    if os.environ.get("RENDER") or os.environ.get("PORT"):
        host = "0.0.0.0"
    server = ThreadingHTTPServer((host, port), MatrixHandler)
    print(f"NumPy Matrix Studio is running at http://{'127.0.0.1' if host == '0.0.0.0' else host}:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping NumPy Matrix Studio...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
