#!/usr/bin/env python3
import os, json, base64, requests

OWNER="WhompINC"; REPO="Files"; BRANCH="main"; TOKEN="ghp_token"
ROOT="d"; FILE="file_tree.json"

def build(p):
    t={}
    for n in sorted(os.listdir(p)):
        fp=os.path.join(p,n)
        if os.path.isdir(fp): t[n]=build(fp)
        else: t[n]="file"
    return t

data={b:build(os.path.join(ROOT,b)) for b in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT,b))}
s=json.dumps(data,indent=2)
with open(FILE,"w") as f: f.write(s)

api="https://api.github.com/repos/WhompINC/Files/contents/"+FILE
h={"Authorization":"Bearer "+TOKEN,"Accept":"application/vnd.github+json"}
r=requests.get(api,headers=h)
sha=r.json().get("sha") if r.status_code==200 else None
payload={"message":"ci:regen","content":base64.b64encode(s.encode()).decode(),"branch":BRANCH}
if sha: payload["sha"]=sha
r2=requests.put(api,headers=h,json=payload)
print(r2.status_code)
