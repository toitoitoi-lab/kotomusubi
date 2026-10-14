# -*- coding: utf-8 -*-
# usage: python3 build_app.py <VERSION> <YYYYMMDD> <dictdir>
import sys,os,json,shutil
ver,date,dd=sys.argv[1:4]
tpl=open('src/app_template.html',encoding='utf-8').read()
def build(variant):
    out=f'build/{variant}'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
    inline=''
    if variant=='private':
        idx=json.load(open(f'{dd}/index.json',encoding='utf-8'))
        dicts={r['id']:json.load(open(f'{dd}/{r["file"]}',encoding='utf-8')) for r in idx['roles']}
        di=json.load(open(f'{dd}/dialect_index.json',encoding='utf-8')) if os.path.exists(f'{dd}/dialect_index.json') else {'regions':[]}
        dials={r['id']:json.load(open(f'{dd}/{r["file"]}',encoding='utf-8')) for r in di['regions']}
        blob=json.dumps({'index':idx,'dicts':dicts,'dialIndex':di,'dialects':dials},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
        inline='<script>window.__KM='+blob+';</script>'
    else:
        shutil.copytree(dd,f'{out}/data')
    html=tpl.replace('{{VERSION}}',ver).replace('{{VARIANT}}',variant).replace('{{INLINE_DATA}}',inline).replace('{{TITLE_SUFFIX}}',' (private)' if variant=='private' else '')
    name=f'kotomusubi_{variant}_index_v{ver}_{date}.html'
    open(f'{out}/{name}','w',encoding='utf-8').write(html)
    shutil.copy(f'{out}/{name}',f'{out}/index.html')
    for f in ['manifest.webmanifest','icon.svg']: shutil.copy('src/'+f,out)
    if variant=='public':
        shutil.copy('src/public_extra/README.md',out); shutil.copytree('src/public_extra/docs',out+'/docs')
    if variant=='public': open(f'{out}/sw.js','w').write(open('src/sw.js').read().replace('{{VERSION}}',ver))
    print(variant,name,os.path.getsize(f'{out}/{name}'))
build('public'); build('private')
