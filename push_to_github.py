#!/usr/bin/env python3
"""Push files to GitHub repo using API - no gh or git needed"""
import urllib.request, urllib.error, json, os, base64

REPO = "zhangfan1014/csm-dashboard-"
BRANCH = "main"
FILES = {}

# Read files to push
base = "/Users/edy/WorkBuddy/2026-07-10-18-07-45"
for path in ["index.html", "api/customers.js", "vercel.json", ".gitignore", "README.md"]:
    full = os.path.join(base, path)
    with open(full, "r") as f:
        content = f.read()
    FILES[path] = content

def push_file(path, content, token=None):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = json.dumps({
        "message": f"Add {path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH
    }).encode()
    
    req = urllib.request.Request(url, data=data, method="PUT")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    try:
        resp = urllib.request.urlopen(req)
        print(f"  OK: {path}")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  FAIL: {path} - {e.code}: {json.loads(body).get('message','')}")
        return False

# Try with env vars
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
print(f"Token available: {'yes' if token else 'no'}")

for path, content in FILES.items():
    push_file(path, content, token)
