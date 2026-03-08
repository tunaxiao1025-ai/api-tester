# Response Format

The request helper always prints three sections in this order:

1. `Status: <code> <reason>`
2. `Headers:`
3. `Body:`

Behavior details:

- Response headers are printed one per line with two leading spaces.
- Empty bodies render as `<empty>`.
- JSON response bodies are pretty-printed with sorted keys.
- Non-JSON response bodies are printed as received after UTF-8 decode with replacement.
