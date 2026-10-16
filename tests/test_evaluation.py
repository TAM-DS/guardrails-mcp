import asyncio
import os
import sys
from types import SimpleNamespace as NS
from unittest.mock import Mock
import pytest
from guardrails_mcp import engine, store
from guardrails_mcp.checks import evaluate
from guardrails_mcp.contracts import Draft

@pytest.fixture(autouse=True)
def isolated(tmp_path,monkeypatch):
    monkeypatch.setenv('GUARDRAILS_DATA_DIR',str(tmp_path))
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)


def test_demo_detects_seeded_regressions_and_persists():
    r=engine.run()
    assert r['summary']['variants']['baseline']['passed']==6
    assert set(r['summary']['regressions'])=={'suppressed','missing-evidence','seller-history'}
    assert store.get(r['id'])==r
    assert r['max_calls']==0

@pytest.mark.parametrize('mode,repeats',[('unknown',1),('demo',0),('demo',4),('demo',True)])
def test_run_bounds(mode,repeats):
    with pytest.raises(ValueError):engine.run(mode,repeats)

def test_live_requires_explicit_cost_acknowledgment():
    with pytest.raises(ValueError,match='acknowledge'):engine.run('live')

def test_live_requires_key():
    with pytest.raises(ValueError,match='API_KEY'):engine.run('live',acknowledge_cost=True)

def test_unknown_source_and_suppression_are_detected():
    c=engine.suite()[0];o=engine.demo_output(c,'baseline');o['claims'][0]['source_id']='invented'
    assert 'source_ids_exist' in evaluate(c,o)['failures']
    assert not evaluate(engine.suite()[1],o)['passed']

def test_schema_rejects_unknown_fields():
    c=engine.suite()[0];o=engine.demo_output(c,'baseline');o['send_now']=True
    assert evaluate(c,o)['failures']==['schema']

def test_semantic_gap_is_explicit():
    c=engine.suite()[0];o=engine.demo_output(c,'baseline')
    o['body']='Your business has 500 factories.'
    assert evaluate(c,o)['passed']  # Deliberately proves these checks do NOT establish factual truth.

def test_provider_failure_is_not_labeled_prompt_regression():
    client=NS(responses=NS(parse=Mock(side_effect=RuntimeError('secret-test-key'))))
    r=engine.run('live',acknowledge_cost=True,client=client)
    assert r['status']=='completed_with_errors'
    assert not r['summary']['regressions']
    assert r['summary']['not_compared_pairs']==6
    assert 'secret-test-key' not in str(r)
    assert client.responses.parse.call_count==12

def test_live_contract_and_usage(monkeypatch):
    monkeypatch.setenv('OPENAI_MODEL','gpt-5-mini')
    c=engine.suite()[0];output=Draft.model_validate(engine.demo_output(c,'baseline'))
    response=NS(status='completed',output_parsed=output,usage=NS(input_tokens=12,output_tokens=20))
    client=NS(responses=NS(parse=Mock(return_value=response)))
    result,tokens,error=engine.live_output(client,'gpt-5-mini','test prompt',c)
    assert not error and tokens=={'input':12,'output':20}
    args=client.responses.parse.call_args.kwargs
    assert args['store'] is False and args['max_output_tokens']==2000 and 'tools' not in args
    assert 'expected' not in args['input'] and 'forbidden' not in args['input']

def test_incomplete_preserves_usage():
    response=NS(status='incomplete',output_parsed=None,usage=NS(input_tokens=5,output_tokens=2000))
    client=NS(responses=NS(parse=Mock(return_value=response)))
    output,tokens,error=engine.live_output(client,'gpt-5-mini','prompt',engine.suite()[0])
    assert output is None and error and tokens['output']==2000

def test_path_input_rejected():
    with pytest.raises(ValueError):store.get('../../.env')

def test_mcp_protocol_subprocess():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    async def check():
        params=StdioServerParameters(command=sys.executable,args=['-m','guardrails_mcp.server'],env={**os.environ})
        async with stdio_client(params) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                listing=await session.list_tools()
                assert {t.name for t in listing.tools}=={'list_cases','run_demo','list_runs','get_run'}
                result=await session.call_tool('run_demo',{})
                assert not result.isError
                records=await session.call_tool('list_runs',{})
                assert not records.isError
                invalid=await session.call_tool('get_run',{'run_id':'../../.env'})
                assert invalid.isError
    asyncio.run(check())

@pytest.mark.parametrize("body", [
    "There are no claims about existing customers or guaranteed outcomes",
    "We deliver guaranteed outcomes.",
])
def test_phrase_match_requires_review_without_guessing_negation(body):
    case = next(c for c in engine.suite() if c["id"] == "source-injection")
    output = engine.demo_output(case, "baseline")
    output["body"] = body
    result = evaluate(case, output)
    assert result["passed"] is False  # Preserve conservative raw scoring.
    assert result["assessment"] == "review"
    assert result["review_required"] and result["hard_failures"] == []
    assert result["phrase_matches"][0]["matched_text"] == "guaranteed"
    assert result["phrase_matches"][0]["excerpt"] == body


def test_review_flag_does_not_hide_suppression_failure():
    case = next(c for c in engine.suite() if c["id"] == "suppressed")
    result = evaluate(case, engine.demo_output(case, "candidate"))
    assert result["assessment"] == "fail"
    assert "expected_decision" in result["hard_failures"]
    assert result["review_required"]


def test_versioned_runs_preserve_old_records():
    legacy = {"id": "a" * 32, "created": store.now(), "status": "completed",
              "mode": "live", "summary": {"variants": {"candidate": {"passed": 1}}}}
    store.save(legacy)
    fresh = engine.run()
    assert fresh["evaluator_version"] == "0.1.1"
    assert fresh["summary"]["variants"]["candidate"]["review_only"] == 1
    assert store.get(legacy["id"]) == legacy
