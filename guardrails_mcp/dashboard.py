import os
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
import gradio as gr
from dotenv import load_dotenv
from .engine import run
from . import store

def refresh():
    runs=store.recent()
    table=[]
    for r in runs:
        s=r.get("summary",{});v=s.get("variants",{})
        table.append([r["id"],r["mode"],r["status"],str(v.get("baseline",{}).get("passed","—")),str(v.get("candidate",{}).get("passed","—")),len(s.get("regressions",[]))])
    return table,gr.update(choices=[r["id"] for r in runs],value=runs[0]["id"] if runs else None),runs[0] if runs else {}

def demo():
    run();return refresh()

def build():
    with gr.Blocks(title="GuardRails-MCP") as app:
        gr.Markdown("# GuardRails-MCP\n### Did the prompt change actually make things better?\nCompare defined cases. Inspect failures. Keep the release decision human.")
        gr.Markdown("**Local prototype · six fictional cases · demo results are seeded · no delivery or deployment authority.** Live runs are explicitly enabled through the CLI only. The dashboard never spends API credits.")
        with gr.Row():
            launch=gr.Button("Run seeded demo",variant="primary")
            reload=gr.Button("Refresh results")
        table=gr.Dataframe(headers=["Run ID","Mode","Status","Baseline passes","Candidate passes","Raw check regression pairs"],interactive=False)
        selection=gr.Dropdown(label="Inspect a recorded run",choices=[])
        details=gr.JSON(label="Evidence, outputs, checks and provenance")
        gr.Markdown("**Review guidance:** Pass counts and regression pairs use raw deterministic checks. A phrase match is a review flag, not proof of an unsafe claim. New records include matched excerpts and a review-only assessment; older records remain unchanged.\n\n**Known gaps:** phrase checks can flag negations or quotations and miss paraphrases; references do not prove claims; no semantic-drift metric or model judge; no statistical confidence from this small suite. Provider errors are reported separately from regressions. Demo timings measure fixture code, not LLM latency. Token totals exclude unreported usage on failed calls.")
        app.load(refresh,outputs=[table,selection,details]);reload.click(refresh,outputs=[table,selection,details]);launch.click(demo,outputs=[table,selection,details]);selection.change(lambda id:store.get(id) if id else {},selection,details)
    return app

def main():
    load_dotenv()
    build().launch(server_name=os.getenv("GUARDRAILS_HOST","127.0.0.1"),server_port=7861,share=False)
if __name__=="__main__":main()

