# -*- coding: utf-8 -*-
# 辞書を立場ごとに分割する。 usage: python3 split_dict.py <dict.json> <outdir>
import json,sys,os,re
src,out=sys.argv[1],sys.argv[2]
d=json.load(open(src,encoding='utf-8'))
os.makedirs(out,exist_ok=True)
by={}
for e in d['expressions']: by.setdefault(e['role'],[]).append(e)
EN_ROLE={'elementary':'Elementary school (Grades 1–6)','juniorhigh':'Junior high (Grades 7–9)','highschool':'High school (Grades 10–12)'}  # 英語版は学年を Grade で表す
idx={'app':d['app'],'dict':d['dict'],'version':d['version'],'built':d['built'],
     'roles':[],'scenes':d['scenes'],'intents':d['intents'],'lunchKinds':d.get('lunchKinds',[]),'lunchDefault':d.get('lunchDefault',{}),'hiddenDefault':d.get('hiddenDefault',{})}
for r in d['roles']:
    rr=dict(r); rr['en']=EN_ROLE.get(r['id'],r['en']); rr['count']=len(by[r['id']]); rr['file']='dict_%s.json'%r['id']; idx['roles'].append(rr)
    rows=[[e['id'],e['scene'],e['intent'],e['level'],e['hira'],e['ruby'],e['en'],e['icon']]+([e['sub']] if e.get('sub') else []) for e in by[r['id']]]
    json.dump({'role':r['id'],'cols':['id','scene','intent','level','hira','ruby','en','icon','sub'],'rows':rows},
              open(os.path.join(out,rr['file']),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
json.dump(idx,open(os.path.join(out,'index.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
tot=sum(os.path.getsize(os.path.join(out,f)) for f in os.listdir(out))
print('files',len(os.listdir(out)),'bytes',tot)
