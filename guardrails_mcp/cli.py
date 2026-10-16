import argparse
import json
from dotenv import load_dotenv
from .engine import run
from . import store

def main():
    load_dotenv()
    parser=argparse.ArgumentParser(description="Bounded prompt evaluation; live calls require explicit consent")
    sub=parser.add_subparsers(dest="command",required=True)
    execute=sub.add_parser("run");execute.add_argument("--mode",choices=["demo","live"],default="demo")
    execute.add_argument("--repeats",type=int,choices=[1,2,3],default=1)
    execute.add_argument("--acknowledge-cost",action="store_true")
    sub.add_parser("list")
    show=sub.add_parser("show");show.add_argument("run_id")
    args=parser.parse_args()
    if args.command=="run":
        record=run(args.mode,args.repeats,args.acknowledge_cost)
        print(json.dumps({k:record[k] for k in ("id","status","mode","summary")},indent=2))
    elif args.command=="show":print(json.dumps(store.get(args.run_id),indent=2))
    else:print(json.dumps([{k:r[k] for k in ("id","status","mode","created")} for r in store.recent()],indent=2))
if __name__=="__main__":main()
