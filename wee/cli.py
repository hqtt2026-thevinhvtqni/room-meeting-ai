from __future__ import annotations
import argparse, json
from pathlib import Path
from .authority import CanonicalWorkAuthority
from .models import WorkContext, EvidenceStore
from .controller import LifecycleController

def main():
    ap=argparse.ArgumentParser(description='Generic ROOM-HOP work_e2e')
    ap.add_argument('authority'); ap.add_argument('--work-id', default=None)
    ap.add_argument('--evidence-root', default=None)
    args=ap.parse_args()
    binding = CanonicalWorkAuthority(args.authority).resolve(args.work_id)
    context = WorkContext.from_binding(binding)
    root = Path(args.evidence_root or binding.evidence_root)
    result = LifecycleController(context, EvidenceStore(root)).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 2)
if __name__=='__main__': main()
