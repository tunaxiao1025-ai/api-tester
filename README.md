# API Tester

An OpenClaw skill for testing HTTP APIs.

## Installation

```bash
clawhub install api-tester
```

## Usage

```bash
# Test a GET request
python3 scripts/api_request.py GET https://httpbin.org/get

# With custom headers
python3 scripts/api_request.py GET https://httpbin.org/headers \
  --header "Authorization: Bearer token"

# POST with JSON body
python3 scripts/api_request.py POST https://httpbin.org/post \
  --json '{"name":"demo"}'
```

## Packaging

```bash
python3 scripts/package_skill.py
```

The skill archive will be created at `dist/api-tester.skill`.
