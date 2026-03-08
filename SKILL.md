---
name: api-tester
description: Send and inspect HTTP requests for API testing workflows. Use when Codex needs to test an HTTP endpoint, compare GET/POST/PUT/DELETE behavior, send an optional JSON body, attach custom headers, or report response status, headers, and body while debugging or validating an API.
---

# API Tester

Use the bundled request script to make direct HTTP calls and print a complete response summary.

## Workflow

1. Decide the HTTP method: `GET`, `POST`, `PUT`, or `DELETE`.
2. Collect the target URL.
3. Add any required headers with repeated `--header` flags.
4. Pass a JSON body only when the endpoint expects one.
5. Run `python3 scripts/api_request.py ...`.
6. Read the printed `Status`, `Headers`, and `Body` sections.

## Request Script

Run the helper directly:

```bash
python3 scripts/api_request.py GET https://httpbin.org/get
python3 scripts/api_request.py POST https://httpbin.org/post --header "Authorization: Bearer token" --json '{"name":"demo"}'
```

Behavior:

- Parse repeated `--header "Name: Value"` flags into request headers.
- Parse `--json` as JSON and send it as the request body.
- Add `Content-Type: application/json` automatically when `--json` is provided and that header is not already set.
- Print response status, response headers, and response body.
- Pretty-print JSON response bodies when possible.
- Return exit code `1` for transport errors and `2` for invalid input such as malformed headers or JSON.

## References

- Read [references/usage.md](/Users/1234/Projects/api-tester/references/usage.md) for common command patterns.
- Read [references/response-format.md](/Users/1234/Projects/api-tester/references/response-format.md) when you need the exact output contract.

## Packaging

Package the skill into a `.skill` archive with:

```bash
python3 scripts/package_skill.py
```

The archive is written to `dist/api-tester.skill`.
