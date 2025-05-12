[1mdiff --git a/README.md b/README.md[m
[1mindex fa48e2b..405a87f 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -1,18 +1,11 @@[m
 # SDU Shield Explorer (Gist-Backed)[m
 [m
[31m-## Setup (one-time)[m
[31m-1. Populate `d/directory_GPT/` and `d/virtual/` with your files.[m
[31m-2. Create a public Gist (as done) containing `file_tree.json`.[m
[31m-3. Set your GitHub token:[m
[31m-   ```[m
[31m-   export GITHUB_TOKEN=ghp_...  # must have gist scope[m
[31m-   ```[m
[32m+[m[32m## Setup[m
[32m+[m[32mPopulate `d/directory_GPT` and `d/virtual` with your files.[m[41m  [m
[32m+[m[32mThen simply run:[m
[32m+[m[32m```[m
[32m+[m[32mpython file_master.py map[m
[32m+[m[32m```[m
[32m+[m[32mto regenerate and publish your map to the Gist.[m
 [m
[31m-## Usage[m
[31m-- **Generate & publish** map:[m
[31m-  ```[m
[31m-  python file_master.py map[m
[31m-  ```[m
[31m-- **Explorer** always fetches latest map from the Gist:[m
[31m-  Open `index.html` in your browser or via GitHub Pages:[m
[31m-  https://whompinc.github.io/Files/[m
[32m+[m[32mOpen `index.html` (e.g. via GitHub Pages) to view.[m
[1mdiff --git a/file_master.py b/file_master.py[m
[1mindex 323b840..2f6ccfe 100644[m
[1m--- a/file_master.py[m
[1m+++ b/file_master.py[m
[36m@@ -2,28 +2,30 @@[m
 import os, json[m
 from github import Github[m
 [m
[31m-GIST_ID = "cdfaad8036ec458507db2eb66da8de2c"[m
[31m-GIST_FILE = "file_tree.json"[m
[31m-DOC_ROOT = "d"[m
[32m+[m[32m# Config[m
[32m+[m[32mGIST_ID   = "cdfaad8036ec458507db2eb66da8de2c"[m
[32m+[m[32mDOC_ROOT  = "d"[m
[32m+[m[32mimport os[m
 TOKEN = os.getenv("GITHUB_TOKEN")[m
[31m-[m
 if not TOKEN:[m
[31m-    raise SystemExit("Set GITHUB_TOKEN with gist scope")[m
[32m+[m[32m    raise SystemExit("Error: please set GITHUB_TOKEN as an environment variable.")[m
[32m+[m
 [m
 def build_tree(path):[m
     tree={}[m
[31m-    for n in sorted(os.listdir(path)):[m
[31m-        f=os.path.join(path,n)[m
[31m-        if os.path.isdir(f):[m
[31m-            tree[n]=build_tree(f)[m
[31m-        else:[m
[31m-            tree[n]="file"[m
[32m+[m[32m    for name in sorted(os.listdir(path)):[m
[32m+[m[32m        full=os.path.join(path,name)[m
[32m+[m[32m        tree[name]=build_tree(full) if os.path.isdir(full) else "file"[m
     return tree[m
 [m
[31m-data={b:build_tree(os.path.join(DOC_ROOT,b)) for b in sorted(os.listdir(DOC_ROOT)) if os.path.isdir(os.path.join(DOC_ROOT,b))}[m
[31m-content=json.dumps(data,indent=2)[m
[32m+[m[32mdata={}[m
[32m+[m[32mfor branch in sorted(os.listdir(DOC_ROOT)):[m
[32m+[m[32m    p=os.path.join(DOC_ROOT,branch)[m
[32m+[m[32m    if os.path.isdir(p):[m
[32m+[m[32m        data[branch]=build_tree(p)[m
 [m
[32m+[m[32mcontent=json.dumps(data,indent=2)[m
 gh=Github(TOKEN)[m
 gist=gh.get_gist(GIST_ID)[m
[31m-gist.edit(files={GIST_FILE:{"content":content}})[m
[31m-print("✅ Gist updated")[m
\ No newline at end of file[m
[32m+[m[32mgist.edit(files={ "file_tree.json": { "content": content } })[m
[32m+[m[32mprint("✅ Gist updated with latest map")[m
\ No newline at end of file[m
[1mdiff --git a/index.html b/index.html[m
[1mindex 01d027f..26d1e6c 100644[m
[1m--- a/index.html[m
[1m+++ b/index.html[m
[36m@@ -11,8 +11,7 @@[m
                "sidebar viewer"; height:100%; }[m
     #sidebar { grid-area: sidebar; background:#2d2d2d; padding:10px; overflow-y:auto; }[m
     #sidebar ul { list-style:none; padding:0; margin:0; }[m
[31m-    #sidebar li { padding:4px; cursor:pointer; transition:background .2s; }[m
[31m-    #sidebar li:hover { background:#3a3a3a; }[m
[32m+[m[32m    #sidebar li { padding:4px; cursor:pointer; }[m
     #header { grid-area: header; display:flex; align-items:center; background:#333; padding:8px; }[m
     #controls { grid-area: controls; display:flex; align-items:center; background:#333; padding:4px 8px; }[m
     #viewer { grid-area: viewer; padding:12px; overflow-y:auto; background:#252526; }[m
[36m@@ -31,7 +30,7 @@[m
     <div id="viewer"><pre id="doc-view">Select a file or folder</pre></div>[m
   </div>[m
   <script>[m
[31m-    const GIST_URL = 'https://gist.githubusercontent.com/WhompINC/cdfaad8036ec458507db2eb66da8de2c/raw/f60e8d360b2460d8e44ea648a58bb2ab3cf2d491/file_tree.json';[m
[32m+[m[32m    const GIST_URL = 'https://gist.githubusercontent.com/WhompINC/cdfaad8036ec458507db2eb66da8de2c/raw/file_tree.json';[m
     let treeData={}, hist=[], pos=-1;[m
     const treeEl=document.getElementById('tree'), viewer=document.getElementById('viewer'),[m
           docView=document.getElementById('doc-view'), pathEl=document.getElementById('path'),[m
[36m@@ -45,30 +44,28 @@[m
       }catch(e){ pathEl.textContent='Failed to load tree'; console.error(e); }[m
     }[m
     function renderSidebar(){[m
[31m-      treeEl.innerHTML=''; for(const [env,node] of Object.entries(treeData)){[m
[31m-        const li=document.createElement('li'); li.textContent=env; li.onclick=e=>navigate(env);[m
[31m-        treeEl.append(li);[m
[32m+[m[32m      treeEl.innerHTML=''; for(const env in treeData){[m
[32m+[m[32m        const li=document.createElement('li'); li.textContent=env;[m
[32m+[m[32m        li.onclick=()=>navigate(env); treeEl.append(li);[m
       }[m
     }[m
     async function navigate(path){[m
[31m-      hist.push(path); pos=hist.length-1; updateNav(); pathEl.textContent=path;[m
[31m-      const [env,...rest]=path.split('/'); let node=treeData[env]; rest.forEach(r=>node=node[r]);[m
[32m+[m[32m      hist.push(path); pathEl.textContent=path;[m
[32m+[m[32m      const [env,...rest]=path.split('/'), node=rest.reduce((n,p)=>n[p], treeData[env]);[m
       viewer.innerHTML=''; if(typeof node==='object'){[m
[31m-        for(const [n,v] of Object.entries(node)){ showItem(env+'/'+n,v); }[m
[32m+[m[32m        for(const name in node) showItem(env+'/'+name,node[name]);[m
       } else {[m
         try{ const r=await fetch(path), t=await r.text(); viewer.innerHTML='<pre>'+t+'</pre>'; }[m
         catch{ docView.textContent='Error loading file'; }[m
       }[m
     }[m
     function showItem(full,val){[m
[31m-      const name=full.split('/').pop(), ext=name.split('.').pop(), icon='📄';[m
[32m+[m[32m      const name=full.split('/').pop(), icon='📄';[m
       const div=document.createElement('div'); div.className='item';[m
       div.innerHTML=`<div class="icon">${icon}</div><div class="name">${name}</div>`;[m
[31m-      div.onclick=_=>navigate(full); viewer.append(div);[m
[32m+[m[32m      div.onclick=()=>navigate(full); viewer.append(div);[m
     }[m
[31m-    function updateNav(){/* no nav buttons here */ }[m
[31m-    refreshBtn.onclick=loadTree; searchBtn.onclick=_=>{}; searchEl.onkeydown=e=>{};[m
[31m-    window.onload=loadTree;[m
[32m+[m[32m    refreshBtn.onclick=loadTree; window.onload=loadTree;[m
   </script>[m
 </body>[m
 </html>[m
\ No newline at end of file[m
