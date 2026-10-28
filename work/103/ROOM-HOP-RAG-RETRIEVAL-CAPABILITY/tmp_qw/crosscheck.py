import json, re
from pathlib import Path
import sys
sys.path.insert(0,'04_CODE')
from rag_retrieval import Document, index_documents, RetrievalIndex

qw=json.load(open('05_TEST/BLIND_LABELS_QW_PASS1.json'))
ev=json.load(open('05_TEST/EVAL_SET.json'))
pool={i['id']:i['query'] for i in ev['items']} if 'items' in ev else None

docs=[Document(d['source_id'],d['title'],d['text']) for d in ev['documents']]
lines={d.source_id:d.text.splitlines() for d in docs}
tok=lambda s:[t.casefold() for t in re.findall(r"[\w'-]+",s)]

def token_support(q, src):
    """Fraction of query tokens that appear anywhere in the doc."""
    qt=set(tok(q)); dt=set()
    for ln in lines[src]: dt|=set(tok(ln))
    miss=sorted(qt-dt)
    return (len(qt)-len(miss))/max(1,len(qt)), miss

print("== Corpus-token support check for items labeled answerable=true ==")
bad=[]
for it in qw['items']:
    if not it['answerable']: continue
    for s in it['expected_source_ids']:
        cov,miss=token_support(it['query'],s)
        flag='' if cov>=0.5 else '  <-- LOW SUPPORT'
        if cov<0.5: bad.append((it['id'],s,round(cov,2),miss))
        print(f"{it['id']} {cov:.2f} {s.split('/')[-1]:32s} missing={miss}{flag}")
print()
print("== Items labeled answerable=false: which docs share >=50% query tokens (potential missed answers) ==")
for it in qw['items']:
    if it['answerable']: continue
    hi=[]
    for s in lines:
        cov,miss=token_support(it['query'],s)
        if cov>=0.6: hi.append((s.split('/')[-1],round(cov,2)))
    print(f"{it['id']} {'|'.join(f'{a}:{b}' for a,b in hi) or '(no doc >=0.6 coverage)'}  q={it['query']}")
