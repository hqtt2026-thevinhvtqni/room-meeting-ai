from __future__ import annotations
import argparse, json
from .authority import CanonicalWorkAuthority
from .models import WorkContext
from .bridge.local_host import LocalExecutionHost

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('authority'); ap.add_argument('--work-id', default=None); args=ap.parse_args()
    binding=CanonicalWorkAuthority(args.authority).resolve(args.work_id); context=WorkContext.from_binding(binding)
    host_report=LocalExecutionHost(binding.evidence_root).discover(context)
    blocked=[cap for cap in host_report['capabilities'] if cap['status'] in ('NOT_CONFIGURED','BLOCKED','FAILED')]
    report={'status':'WEE READY' if not blocked else 'WEE BLOCKED','work_id':context.work_id,'execution_id':context.execution_id,'capabilities':host_report['capabilities'],'blockers':blocked}
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if not blocked else 2)
if __name__=='__main__': main()
