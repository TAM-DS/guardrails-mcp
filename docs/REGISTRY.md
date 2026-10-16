# Registry readiness — planned, not registered

The first release targets local stdio distribution. A working demo is not a registry listing.

Before publishing:

1. Validate the Mac client and Docker startup paths.
2. Choose distribution rights deliberately; no license is currently included.
3. Publish a versioned package to PyPI or an OCI image to a supported registry such as GHCR.
4. Add ownership metadata required by the official MCP Registry.
5. Generate and validate server.json against the then-current schema, using the actual package/image identifier and supported transport.
6. Authenticate the publisher namespace, publish, and verify retrieval and clean-machine installation.

Keep registry metadata truthful: six fictional cases, local prototype, seeded demo versus opt-in live evaluation, and no deployment authority. Do not describe this as an OWASP security scanner or a NIST-certified product.

Requirements: https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md
