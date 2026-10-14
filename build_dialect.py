# -*- coding: utf-8 -*-
# usage: python3 build_dialect.py <dictdir>   (src/dialect の regions.json と packs/*.csv から data/dialect_*.json を作る)
import sys,os,json,csv,glob,collections,re
dd=sys.argv[1]
regions=json.load(open('src/dialect/regions.json',encoding='utf-8'))
out=[]
for r in regions:
    p=f'src/dialect/packs/{r["id"]}.csv'; rows=[]
    if os.path.exists(p):
        for x in csv.DictReader(open(p,encoding='utf-8')):
            if x['standard_hira'].strip() and x['dialect_hira'].strip(): rows.append([x['standard_hira'].strip(),x['dialect_hira'].strip()])
    rp=f'src/dialect/rules/{r["id"]}.json'; rules=[]
    if os.path.exists(rp):
        for pat,rep in json.load(open(rp,encoding='utf-8')): rules.append([pat,re.sub(r'\\(\d)',r'$\1',rep)])
    r=dict(r,count=len(rows),rules=len(rules),status='draft' if (rows or rules) else 'wanted',file=f'dialect_{r["id"]}.json')
    json.dump({'id':r['id'],'rows':rows,'rules':rules},open(f'{dd}/{r["file"]}','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    out.append(r)
json.dump({'regions':out},open(f'{dd}/dialect_index.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
# 確認用シート：よく使う標準語のことばを短い順に並べる
rows=[]
for f in glob.glob(f'{dd}/dict_*.json'):
    rows+=json.load(open(f,encoding='utf-8'))['rows']
cnt=collections.Counter(); ruby={}
for r in rows: cnt[r[4]]+=1; ruby.setdefault(r[4],r[5])
cand=sorted(cnt, key=lambda h:(-cnt[h], len(h)))
cand=[h for h in cand if len(h.replace(' ',''))<=14][:300]
os.makedirs('out',exist_ok=True)
with open('out/dialect_review_template.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['standard_hira','漢字まじり','dialect_hira（その地域のことば・ひらがな）','メモ（ていねいさ・使う場面・ことなる言い方）'])
    for h in cand: w.writerow([h,ruby[h].replace('[','（').replace(']','）') if False else ruby[h],'',''])
print(len(out),'regions',len(cand),'review rows')
