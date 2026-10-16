"""Offline integration check against an actual SignalDesk checkout. Uses a temporary DB only."""
import argparse
import json
import sys
import tempfile
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--checkout",required=True);args=parser.parse_args()
    checkout=Path(args.checkout).resolve()
    if not (checkout/"app/main.py").is_file():raise SystemExit("Not a SignalDesk checkout")
    sys.path.insert(0,str(checkout))
    from fastapi.testclient import TestClient
    from app.main import create_app
    from guardrails_mcp.checks import evaluate
    with tempfile.TemporaryDirectory() as directory:
        with TestClient(create_app(f"sqlite:///{directory}/signaldesk.db")) as client:
            leads=client.get('/api/leads').json()
            meridian=next(x for x in leads if x['id']=='avery')
            case={'expected':'draft','input':{'sources':meridian['sources']},'forbidden':[r'your wife',r'guaranteed']}
            checked=evaluate(case,{'decision':'draft','subject':meridian['subject'],'body':meridian['body'],'claims':meridian['claims']})
            suppressed=next(x for x in leads if x['id']=='taylor')
            blocked=client.post('/api/leads/taylor/approve',json={'revision':suppressed['revision']})
            result={'mode':'actual-signaldesk-fixture-integration','draft_checks':checked,'suppressed_approval_http':blocked.status_code,
                    'passed':checked['passed'] and blocked.status_code==409,
                    'scope':'Actual app fixtures and API in a temporary database; no live research, production hook, or customer records.'}
            print(json.dumps(result,indent=2))
            if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
