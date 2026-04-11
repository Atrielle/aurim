from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .commands import known_runs, read_run_status, read_sequence_report, run_regression, run_runner_command, run_sequence, sequence_names
from .page import HTML_PAGE


def _json_response(handler: BaseHTTPRequestHandler, payload: dict, status: int = HTTPStatus.OK) -> None:
    encoded = json.dumps(payload).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)


def _html_response(handler: BaseHTTPRequestHandler, html: str, status: int = HTTPStatus.OK) -> None:
    encoded = html.encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'text/html; charset=utf-8')
    handler.send_header('Content-Length', str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)


def _read_payload(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get('Content-Length', '0'))
    raw = handler.rfile.read(length).decode('utf-8') if length else '{}'
    if handler.headers.get('Content-Type', '').startswith('application/json'):
        return json.loads(raw or '{}')
    return {key: values[-1] for key, values in parse_qs(raw).items()}


class HarnessUIHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == '/':
            _html_response(self, HTML_PAGE)
            return
        if parsed.path == '/api/runs':
            _json_response(self, {'runs': known_runs()})
            return
        if parsed.path == '/api/sequences':
            _json_response(self, {'presets': sequence_names()})
            return
        if parsed.path == '/api/sequence-report':
            ref = parse_qs(parsed.query).get('ref', [''])[-1].strip()
            try:
                payload = read_sequence_report(ref)
            except ValueError as exc:
                _json_response(self, {'error': str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            _json_response(self, payload)
            return
        if parsed.path == '/api/run-status':
            run_id = parse_qs(parsed.query).get('run_id', [''])[-1].strip()
            try:
                payload = read_run_status(run_id)
            except ValueError as exc:
                _json_response(self, {'error': str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            _json_response(self, payload)
            return
        _json_response(self, {'error': 'not found'}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        payload = _read_payload(self)

        if parsed.path == '/api/run-command':
            try:
                result = run_runner_command(
                    command_name=str(payload.get('command', '')).strip(),
                    run_id=str(payload.get('run_id', '')).strip(),
                    unit_id=str(payload.get('unit_id', '')).strip(),
                    report_path=str(payload.get('report', '')).strip(),
                )
            except ValueError as exc:
                _json_response(self, {'error': str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            _json_response(self, result)
            return


        if parsed.path == '/api/run-sequence':
            try:
                result = run_sequence(
                    run_id=str(payload.get('run_id', '')).strip(),
                    preset=str(payload.get('preset', '')).strip() or None,
                )
            except ValueError as exc:
                _json_response(self, {'error': str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            _json_response(self, result)
            return

        if parsed.path == '/api/run-regression':
            _json_response(self, run_regression())
            return

        _json_response(self, {'error': 'not found'}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, fmt: str, *args) -> None:
        return


def serve(host: str = '127.0.0.1', port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), HarnessUIHandler)
    print(f'Harness UI running on http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down Harness UI.')
