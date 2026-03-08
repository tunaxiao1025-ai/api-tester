# API Tester CLI

A simple Python command-line tool for testing HTTP APIs.

## Features

- Supports `GET`, `POST`, `PUT`, and `DELETE`
- Accepts custom headers
- Accepts an optional JSON request body
- Prints response status, headers, and body with readable formatting

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

Run the CLI through the installed command:

```bash
api-tester GET https://httpbin.org/get
```

Send custom headers:

```bash
api-tester GET https://httpbin.org/headers \
  -H "Accept: application/json" \
  -H "X-Debug: true"
```

Send a JSON body:

```bash
api-tester POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  --json '{"name":"demo","enabled":true}'
```

Set a timeout:

```bash
api-tester DELETE https://httpbin.org/delete --timeout 10
```

## Running tests

```bash
pytest
```
