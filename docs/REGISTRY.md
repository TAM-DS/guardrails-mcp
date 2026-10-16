# Registry preparation — not registered

The root server.json targets PyPI package guardrails-mcp 0.1.1 and namespace io.github.TAM-DS/guardrails-mcp. It uses local stdio and an explicitly configured writable data directory. The README contains the matching mcp-name ownership marker and is included in package metadata.

The manifest has been checked against the official 2025-12-11 JSON Schema. This does not validate ownership, package availability or server-side acceptance. GitHub namespace authentication and an existing public PyPI package are still required. The PyPI name returned HTTP 404 during preparation on October 16, 2026; it is not reserved.

See [release steps](RELEASE.md). The package is not yet published and no registry listing is claimed. Current local installation remains supported from this repository.

Sources checked October 16, 2026:
- https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md
- https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/package-types.mdx
- https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json

Keep descriptions bounded: six fictional cases, seeded demo versus opt-in live evaluation, phrase review flags, known gaps, no deployment authority. This is not an OWASP security scanner or a NIST-certified product.
