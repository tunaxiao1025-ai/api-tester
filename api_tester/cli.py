from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import sys
from typing import Any
from urllib import error, request


SUPPORTED_METHODS = ("GET", "POST", "PUT", "DELETE")


@dataclass
class ResponseData:
    status_code: int
    reason: str
    headers: dict[str, str]
    text: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple API testing CLI")
    parser.add_argument("method", choices=SUPPORTED_METHODS, help="HTTP method")
    parser.add_argument("url", help="Request URL")
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        default=[],
        help='Custom header in the form "Name: Value"',
    )
    parser.add_argument(
        "-j",
        "--json",
        dest="json_body",
        help="JSON request body as a string",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds",
    )
    return parser.parse_args(argv)


def parse_headers(header_values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for value in header_values:
        if ":" not in value:
            raise ValueError(f"Invalid header format: {value!r}")
        name, header_value = value.split(":", 1)
        name = name.strip()
        header_value = header_value.strip()
        if not name:
            raise ValueError(f"Invalid header name: {value!r}")
        headers[name] = header_value
    return headers


def parse_json_body(json_body: str | None) -> Any:
    if json_body is None:
        return None
    try:
        return json.loads(json_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON body: {exc.msg}") from exc


def format_body(response: ResponseData) -> str:
    text = response.text
    if not text:
        return "<empty>"

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return text

    return json.dumps(parsed, indent=2, sort_keys=True)


def print_response(response: ResponseData) -> None:
    print(f"Status: {response.status_code} {response.reason}")
    print("Headers:")
    for name, value in response.headers.items():
        print(f"  {name}: {value}")
    print("Body:")
    print(format_body(response))


def build_request(args: argparse.Namespace) -> request.Request:
    headers = parse_headers(args.header)
    json_body = parse_json_body(args.json_body)
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
    return request.Request(
        url=args.url,
        data=data,
        headers=headers,
        method=args.method,
    )


def read_response(http_response) -> ResponseData:
    body = http_response.read().decode("utf-8", errors="replace")
    return ResponseData(
        status_code=http_response.getcode(),
        reason=getattr(http_response, "reason", ""),
        headers=dict(http_response.headers.items()),
        text=body,
    )


def run_request(args: argparse.Namespace) -> int:
    req = build_request(args)

    try:
        with request.urlopen(req, timeout=args.timeout) as http_response:
            response = read_response(http_response)
    except error.HTTPError as exc:
        response = read_response(exc)
    except error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    print_response(response)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        return run_request(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
