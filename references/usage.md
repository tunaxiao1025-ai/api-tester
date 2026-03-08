# API Tester Usage

## Supported methods

- `GET`
- `POST`
- `PUT`
- `DELETE`

## Common commands

Fetch an endpoint:

```bash
python3 scripts/api_request.py GET https://httpbin.org/get
```

Send headers:

```bash
python3 scripts/api_request.py GET https://httpbin.org/headers \
  --header "Accept: application/json" \
  --header "X-Debug: true"
```

Send a JSON body:

```bash
python3 scripts/api_request.py POST https://httpbin.org/post \
  --header "Authorization: Bearer token" \
  --json '{"name":"demo","enabled":true}'
```

Override timeout:

```bash
python3 scripts/api_request.py DELETE https://httpbin.org/delete --timeout 10
```

## Notes

- Repeat `--header` for multiple headers.
- Pass `--json` only with valid JSON text.
- The script prints response status, response headers, and body in separate sections.
