"""Local stdio MCP. No paid provider calls or arbitrary path/command tools."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from dotenv import load_dotenv
from .engine import run, suite
from . import store

server=FastMCP("GuardRails-MCP")
READ=ToolAnnotations(readOnlyHint=True,destructiveHint=False,openWorldHint=False)

@server.tool(annotations=READ)
def list_cases() -> dict:
    """List the six fictional, labeled cases and evaluation limitations."""
    return {"cases":[{"id":c["id"],"expected":c["expected"]} for c in suite()],
            "scope":"Deterministic checks; no complete semantic verification or deployment authority."}

@server.tool(annotations=ToolAnnotations(readOnlyHint=False,destructiveHint=False,openWorldHint=False))
def run_demo() -> dict:
    """Run seeded fixtures with zero API calls; persist a local run. This is not model performance."""
    r=run()
    return {"id":r["id"],"mode":r["mode"],"summary":r["summary"]}

@server.tool(annotations=READ)
def list_runs() -> list[dict]:
    """List up to 30 local runs; running records can be stale after a hard crash."""
    return [{k:r[k] for k in ("id","status","mode","created")} for r in store.recent()]

@server.tool(annotations=READ)
def get_run(run_id: str) -> dict:
    """Read one local run, including checks, outputs, provenance, and known limitations."""
    return store.get(run_id)

def main():
    load_dotenv()
    server.run(transport="stdio")
if __name__=="__main__":main()
