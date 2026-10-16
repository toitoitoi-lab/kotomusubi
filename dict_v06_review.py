# -*- coding: utf-8 -*-
# 辞書 v0.6：学校の全立場に「振り返り・話し合い」（自己評価・他者評価・意見交換）の場面を足す
# usage: python3 dict_v06_review.py → kotomusubi_public_dict_v0.6_20261016.json と レビュー用CSV
import json,re,csv
SRC='kotomusubi_public_dict_v0.5_20261014.json'; OUT='kotomusubi_public_dict_v0.6_20261016.json'
d=json.load(open(SRC,encoding='utf-8'))
KJ=re.compile(r'([一-鿿々〆ヶ]+)\[([^\]]+)\]')
hira=lambda r:KJ.sub(r'\2',r); kanji=lambda r:re.sub(r'\[[^\]]*\]','',r)
R=[
# 自己評価
('tell',1,'とても よく できました','I did very well.','🌟'),
('tell',1,'まあまあ できました','I did okay.','🙂'),
('tell',2,'あまり できませんでした','I did not do very well.','😕'),
('tell',1,'自分[じぶん]で できました','I did it by myself.','💪'),
('tell',2,'手伝[てつだ]って もらって できました','I did it with help.','🤝'),
('tell',2,'ここが 難[むずか]しかったです','This part was difficult.','🧗'),
('tell',2,'次[つぎ]は ここを がんばりたいです','Next time I want to work on this.','🎯'),
# 意見
('tell',2,'わたしは 賛成[さんせい]です','I agree.','👍'),
('tell',2,'わたしは 反対[はんたい]です','I disagree.','👎'),
('tell',1,'前[まえ]の 人[ひと]と 同[おな]じ 考[かんが]えです','I think the same as the last person.','🟰'),
('tell',2,'少[すこ]し ちがう 考[かんが]えです','My idea is a little different.','🔀'),
('tell',2,'わたしの 考[かんが]えを 言[い]います','I will share my idea.','💡'),
# 他者評価
('tell',1,'今[いま]の 発表[はっぴょう]は よかったです','That presentation was good.','👏'),
('tell',1,'声[こえ]が 聞[き]きやすかったです','Your voice was easy to hear.','👂'),
('tell',1,'絵[え]や 写真[しゃしん]が わかりやすかったです','The pictures were easy to understand.','🖼️'),
('tell',1,'いい 考[かんが]えだと 思[おも]います','I think that is a good idea.','💡'),
('tell',2,'もう少[すこ]し ゆっくり 話[はな]すと いいと 思[おも]います','It might be better to speak a little slower.','🐢'),
# 気持ち
('feeling',1,'楽[たの]しかったです','It was fun.','😊'),
('feeling',1,'できて うれしいです','I am happy I could do it.','😄'),
('feeling',2,'くやしかったです','I was frustrated.','😤'),
('feeling',1,'もっと やりたいです','I want to do more.','🙌'),
('feeling',2,'みんなの 前[まえ]だと 緊張[きんちょう]します','I get nervous in front of everyone.','😬'),
# たずねる
('question',2,'どうして そう 思[おも]いましたか','Why do you think so?','❓'),
('question',1,'どこが よかったですか','What part was good?','❓'),
('question',2,'次[つぎ]は どうすれば いいですか','What should I do next time?','❓'),
('question',2,'わたしの 考[かんが]えを 聞[き]いて もらえますか','Could you listen to my idea?','🙋'),
# たのむ
('request',2,'発表[はっぴょう]したいです','I want to present.','🙋'),
('request',2,'考[かんが]える 時間[じかん]を ください','Please give me time to think.','⏳'),
('request',2,'選[えら]んで 答[こた]えたいです','I would like to answer by choosing.','☑️'),
('request',2,'代[か]わりに 読[よ]んで ください','Please read it for me.','🗣️'),
('request',1,'書[か]いて 見[み]せたいです','I want to show it in writing.','✍️'),
('request',2,'もう少[すこ]し くわしく 教[おし]えて ください','Please tell me in more detail.','🔍'),
# ことわる
('refuse',2,'今[いま]は 発表[はっぴょう]したくないです','I do not want to present right now.','🙅'),
('refuse',1,'パスします','I will pass.','⏭️'),
('refuse',1,'まだ 決[き]まって いません','I have not decided yet.','🤔'),
('refuse',3,'その 意見[いけん]には 反対[はんたい]です','I am against that opinion.','✋'),
# あいさつ
('greet',1,'発表[はっぴょう]を はじめます','I will start my presentation.','🎤'),
('greet',1,'これで 終[お]わります','That is all.','🏁'),
('greet',1,'聞[き]いて くれて ありがとうございました','Thank you for listening.','🙏'),
# こまった
('trouble',2,'考[かんが]えが まとまりません','I cannot put my thoughts together.','🌀'),
('trouble',2,'何[なに]を 言[い]えば いいか わかりません','I do not know what to say.','😥'),
# もういちど
('again',1,'もう一度[いちど] 質問[しつもん]を 言[い]って ください','Please say the question again.','🔁'),
('again',1,'今[いま]の 意見[いけん]を もう一度[いちど] お願[ねが]いします','Please say that opinion again.','🔁'),
]
SCENE={'id':'review','ruby':'振[ふ]り返[かえ]り・話[はな]し合[あ]い','en':'Reflection / discussion','icon':'💬'}
SCENE['hira']=hira(SCENE['ruby']); SCENE['kanji']=kanji(SCENE['ruby'])
ROLES=['elementary','juniorhigh','highschool','college']
scenes=[]
for s in d['scenes']:
    scenes.append(s)
    if s['role'] in ROLES and s['id'] in ('class','lecture'):
        n=dict(SCENE); n['role']=s['role']; scenes.append(n)
E=list(d['expressions'])
for role in ROLES:
    for k,(it,lv,rb,en,ic) in enumerate(R,1):
        E.append({'id':f'{role}_review_{it}_{k:02d}','role':role,'scene':'review','intent':it,'level':lv,'hira':hira(rb),'kanji':kanji(rb),'ruby':rb,'en':en,'icon':ic})
d['version']='0.6'; d['built']='20261016'; d['scenes']=scenes; d['expressions']=E
ids=[e['id'] for e in E]; assert len(ids)==len(set(ids))
json.dump(d,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
with open('kotomusubi_public_dict-review_v0.6_20261016.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['場面','意図','強さ','漢字かな','ふりがな付き','ひらがな','English','直したほうがよい点'])
    for it,lv,rb,en,ic in R: w.writerow(['振り返り・話し合い',it,lv,kanji(rb),rb,hira(rb),en,''])
print('expressions',len(d['expressions']),'added',len(R)*len(ROLES))
