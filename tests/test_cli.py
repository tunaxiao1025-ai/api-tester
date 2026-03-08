import argparse
import io

import pytest
from urllib import error

from api_tester import cli


class DummyResponse:
    def __init__(self, *, status_code=200, reason="OK", headers=None, text=""):
        self.status_code = status_code
        self.reason = reason
        self.headers = headers or {}
        self.text = text


class DummyHTTPResponse:
    def __init__(self, *, status_code=200, reason="OK", headers=None, body=""):
        self._status_code = status_code
        self.reason = reason
        self.headers = headers or {}
        self._body = body.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def getcode(self):
        return self._status_code

    def read(self):
        return self._body


def test_parse_headers_supports_multiple_values():
    headers = cli.parse_headers(["Accept: application/json", "X-Test: 123"])
    assert headers == {"Accept": "application/json", "X-Test": "123"}


def test_parse_headers_rejects_invalid_input():
    with pytest.raises(ValueError, match="Invalid header format"):
        cli.parse_headers(["BrokenHeader"])


def test_parse_json_body_returns_python_data():
    assert cli.parse_json_body('{"name":"demo"}') == {"name": "demo"}


def test_parse_json_body_rejects_bad_json():
    with pytest.raises(ValueError, match="Invalid JSON body"):
        cli.parse_json_body("{bad json}")


def test_format_body_pretty_prints_json():
    response = DummyResponse(
        headers={"Content-Type": "application/json"},
        text='{"name":"demo"}',
    )
    assert cli.format_body(response) == '{\n  "name": "demo"\n}'


def test_format_body_returns_plain_text_for_non_json():
    response = DummyResponse(text="plain text response")
    assert cli.format_body(response) == "plain text response"


def test_print_response_outputs_status_headers_and_body(capsys):
    response = DummyResponse(
        status_code=201,
        reason="Created",
        headers={"Content-Type": "application/json"},
        text='{"id":1}',
    )
    cli.print_response(response)
    captured = capsys.readouterr()
    assert "Status: 201 Created" in captured.out
    assert "Headers:" in captured.out
    assert "Content-Type: application/json" in captured.out
    assert '"id": 1' in captured.out


def test_build_request_passes_method_headers_and_json_body():
    args = argparse.Namespace(
        method="POST",
        url="https://example.com",
        header=["Authorization: Bearer token"],
        json_body='{"hello":"world"}',
        timeout=5.0,
    )

    req = cli.build_request(args)

    assert req.get_method() == "POST"
    assert req.full_url == "https://example.com"
    assert req.headers["Authorization"] == "Bearer token"
    assert req.headers["Content-type"] == "application/json"
    assert req.data == b'{"hello": "world"}'


def test_run_request_prints_successful_response(monkeypatch, capsys):
    def fake_urlopen(req, timeout):
        assert req.get_method() == "POST"
        assert timeout == 5.0
        return DummyHTTPResponse(
            headers={"Content-Type": "application/json"},
            body='{"ok":true}',
        )

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)
    args = argparse.Namespace(
        method="POST",
        url="https://example.com",
        header=["Authorization: Bearer token"],
        json_body='{"hello":"world"}',
        timeout=5.0,
    )

    exit_code = cli.run_request(args)

    assert exit_code == 0
    assert "Status: 200 OK" in capsys.readouterr().out


def test_run_request_prints_http_error_response(monkeypatch, capsys):
    def fake_urlopen(_req, _timeout):
        raise error.HTTPError(
            url="https://example.com",
            code=404,
            msg="Not Found",
            hdrs={"Content-Type": "application/json"},
            fp=io.BytesIO(b'{"detail":"missing"}'),
        )

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)
    args = argparse.Namespace(
        method="GET",
        url="https://example.com",
        header=[],
        json_body=None,
        timeout=5.0,
    )

    exit_code = cli.run_request(args)

    assert exit_code == 0
    assert "Status: 404 Not Found" in capsys.readouterr().out


def test_run_request_returns_error_code_on_url_error(monkeypatch, capsys):
    def fake_urlopen(_req, _timeout):
        raise error.URLError("boom")

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)
    args = argparse.Namespace(
        method="GET",
        url="https://example.com",
        header=[],
        json_body=None,
        timeout=5.0,
    )

    exit_code = cli.run_request(args)

    assert exit_code == 1
    assert "Request failed: <urlopen error boom>" in capsys.readouterr().err


def test_main_returns_validation_error_for_invalid_header(capsys):
    exit_code = cli.main(["GET", "https://example.com", "-H", "BrokenHeader"])
    assert exit_code == 2
    assert "Invalid header format" in capsys.readouterr().err
