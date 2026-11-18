"""Local hold-shelf page and API. The standard library is the only dependency."""

from __future__ import annotations

import json
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlparse

from holdshelf.catalog import Catalog
from holdshelf.overdue import select_overdue, validate_days

STATIC = Path(__file__).resolve().parent / "static" / "index.html"
HOST = "127.0.0.1"
PORT = 8765


class ShelfApp:
    def __init__(
        self, catalog: Catalog | None = None, today: date | None = None
    ) -> None:
        self.catalog = catalog if catalog is not None else Catalog()
        self._today = today

    def handle(self, method: str, target: str) -> tuple[int, object]:
        parsed_target = urlparse(target)
        path = unquote(parsed_target.path)
        if method == "GET" and path == "/api/health":
            return 200, {"status": "ok"}
        if method == "GET" and path == "/api/holds":
            return 200, {"holds": self.catalog.list_holds()}
        if method == "GET" and path == "/api/holds/overdue":
            return self._overdue(parsed_target.query)
        if method == "POST" and path.startswith("/api/holds/") and path.endswith("/pickup"):
            hold_id = path.removeprefix("/api/holds/").removesuffix("/pickup").strip("/")
            return self._pickup(hold_id)
        if method == "GET" and path == "/":
            return 200, STATIC.read_text(encoding="utf-8")
        return 404, {"error": "That page or hold was not found."}

    def _overdue(self, query: str) -> tuple[int, dict]:
        days_values = [value for key, value in parse_qsl(
            query, keep_blank_values=True
        ) if key == "days"]
        if len(days_values) > 1:
            return 400, {"error": "days must be a positive integer"}
        try:
            days = validate_days(days_values[0] if days_values else None)
        except ValueError as error:
            return 400, {"error": str(error)}
        return 200, {
            "holds": select_overdue(
                self.catalog.list_holds(), days, today=self._today
            )
        }

    def _pickup(self, hold_id: str) -> tuple[int, dict]:
        if not hold_id:
            return 400, {"error": "A hold id is required."}
        outcome, hold = self.catalog.mark_picked_up(hold_id)
        if outcome == "missing":
            return 404, {"error": f"Hold {hold_id} was not found."}
        if outcome == "already":
            return 409, {"error": f"Hold {hold_id} is already picked up."}
        return 200, {"hold": hold}


def serve(host: str = HOST, port: int = PORT, catalog: Catalog | None = None) -> None:
    app = ShelfApp(catalog)
    handler = _handler_for(app)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Hold shelf at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def _handler_for(app: ShelfApp):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            self._respond()

        def do_POST(self) -> None:  # noqa: N802
            self._respond()

        def _respond(self) -> None:
            status, payload = app.handle(self.command, self.path)
            if isinstance(payload, str):
                body = payload.encode("utf-8")
                content_type = "text/html; charset=utf-8"
            else:
                body = json.dumps(payload).encode("utf-8")
                content_type = "application/json"
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt: str, *args) -> None:
            return

    return Handler
