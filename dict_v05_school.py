# -*- coding: utf-8 -*-
# 辞書 v0.5：学校の場面を「共通＋学校種に特有」に作り直す（設計書 23章）
# usage: python3 dict_v05_school.py  → kotomusubi_public_dict_v0.5_20261014.json と レビュー用CSV
import json,re,csv,copy
SRC='kotomusubi_public_dict_v0.4_20261010.json'
OUT='kotomusubi_public_dict_v0.5_20261014.json'
d=json.load(open(SRC,encoding='utf-8'))
KJ=re.compile(r'([一-鿿々〆ヶ]+)\[([^\]]+)\]')
hira=lambda r:KJ.sub(r'\2',r)
kanji=lambda r:re.sub(r'\[[^\]]*\]','',r)

# ---- 新しく書いた表現（intent, level, ruby, en, icon） ----
NEW={
'bus':[
('request',2,'バスの 乗[の]り降[お]りを 手伝[てつだ]って ください','Please help me get on and off the bus.','🚌'),
('request',2,'シートベルトを 締[し]めて ください','Please fasten my seat belt.','💺'),
('request',1,'窓[まど]を 開[あ]けて ください','Could you open the window?','🪟'),
('request',1,'窓[まど]を 閉[し]めて ください','Could you close the window?','🪟'),
('request',2,'前[まえ]の 席[せき]に 座[すわ]りたいです','I would like to sit in the front.','💺'),
('request',1,'エアコンを 弱[よわ]く して ください','Please turn the air conditioner down.','❄️'),
('tell',2,'今日[きょう]は バスに 乗[の]りません','I am not taking the bus today.','🚌'),
('tell',2,'明日[あした]は 休[やす]みます','I will be absent tomorrow.','📅'),
('tell',2,'家[いえ]の 人[ひと]が 迎[むか]えに 来[き]ます','Someone from my family is picking me up.','🏠'),
('tell',2,'忘[わす]れ物[もの]を しました','I left something behind.','🎒'),
('question',2,'バスは 何時[なんじ]に 来[き]ますか','What time does the bus come?','🕒'),
('question',2,'あと どのくらいで 着[つ]きますか','How long until we arrive?','⏳'),
('question',1,'今日[きょう]の 運転手[うんてんしゅ]さんは だれですか','Who is the driver today?','🧑‍✈️'),
('question',1,'次[つぎ]は どこに 止[と]まりますか','Where is the next stop?','🚏'),
('refuse',2,'今[いま]は 話[はな]したくないです','I do not want to talk right now.','🤐'),
('refuse',1,'席[せき]は ここで いいです','This seat is fine.','💺'),
('refuse',1,'手伝[てつだ]いは 大丈夫[だいじょうぶ]です','I am okay without help.','👌'),
('refuse',3,'となりに 座[すわ]らないで ください','Please do not sit next to me.','✋'),
('feeling',1,'バスに 乗[の]るのが 楽[たの]しいです','I enjoy riding the bus.','😊'),
('feeling',2,'今日[きょう]は 疲[つか]れました','I am tired today.','😩'),
('feeling',3,'うるさくて つらいです','It is too noisy and hard for me.','🙉'),
('feeling',2,'早[はや]く 帰[かえ]りたいです','I want to get home soon.','🏠'),
('greet',1,'おはようございます','Good morning.','🌅'),
('greet',1,'よろしく お願[ねが]いします','Thank you in advance.','🙇'),
('greet',1,'ありがとうございました','Thank you very much.','🙏'),
('greet',1,'さようなら、 また 明日[あした]','Goodbye, see you tomorrow.','👋'),
('trouble',2,'気分[きぶん]が 悪[わる]いです','I feel sick.','🤢'),
('trouble',2,'バスに 酔[よ]いました','I feel carsick.','🤢'),
('trouble',3,'トイレに 行[い]きたいです。 止[と]めて ください','I need the toilet. Please stop the bus.','🚻'),
('trouble',2,'ベルトが きついです','The belt is too tight.','😣'),
('trouble',3,'けがを しました','I got hurt.','🩹'),
('again',2,'もう一度[いちど] 言[い]って ください','Please say that again.','🔁'),
('again',2,'ゆっくり 話[はな]して ください','Please speak slowly.','🐢'),
('again',2,'聞[き]こえませんでした','I could not hear you.','👂'),
],
'care':[
('request',2,'姿勢[しせい]を 直[なお]して ください','Please help me fix my posture.','🪑'),
('request',2,'体[からだ]の 向[む]きを 変[か]えて ください','Please change my position.','🔄'),
('request',2,'車[くるま]いすを 押[お]して ください','Please push my wheelchair.','🧑‍🦽'),
('request',2,'車[くるま]いすの ブレーキを かけて ください','Please put on my wheelchair brakes.','🧑‍🦽'),
('request',2,'トイレの 介助[かいじょ]を お願[ねが]いします','I need help with the toilet, please.','🚻'),
('request',2,'水[みず]を 飲[の]ませて ください','Please help me drink some water.','🥤'),
('request',1,'クッションを 入[い]れて ください','Please put a cushion in.','🛋️'),
('request',2,'足[あし]の 位置[いち]を 直[なお]して ください','Please adjust my feet.','🦶'),
('request',1,'手[て]を 少[すこ]し 支[ささ]えて ください','Please support my hand a little.','✋'),
('request',2,'ゆっくり 動[うご]かして ください','Please move me slowly.','🐢'),
('request',1,'もう少[すこ]し 右[みぎ]です','A little more to the right.','➡️'),
('request',1,'もう少[すこ]し 左[ひだり]です','A little more to the left.','⬅️'),
('request',1,'もう少[すこ]し 上[うえ]です','A little higher.','⬆️'),
('request',1,'もう少[すこ]し 下[した]です','A little lower.','⬇️'),
('tell',1,'寒[さむ]いです','I am cold.','🥶'),
('tell',1,'暑[あつ]いです','I am hot.','🥵'),
('tell',2,'同[おな]じ 姿勢[しせい]で 疲[つか]れました','I am tired from staying in the same position.','😩'),
('tell',2,'足[あし]が しびれています','My legs are numb.','🦵'),
('tell',1,'自分[じぶん]で やってみます','I will try it myself.','💪'),
('question',1,'今[いま] 何[なに]を しますか','What are we doing now?','❓'),
('question',1,'どこに 移動[いどう]しますか','Where are we going?','📍'),
('question',2,'次[つぎ]の 休憩[きゅうけい]は いつですか','When is the next break?','⏰'),
('refuse',1,'まだ 大丈夫[だいじょうぶ]です','I am still okay.','👌'),
('refuse',3,'今[いま]は 触[さわ]らないで ください','Please do not touch me right now.','✋'),
('refuse',2,'自分[じぶん]で できます','I can do it myself.','💪'),
('refuse',3,'その やり方[かた]は 痛[いた]いです','That way hurts.','😣'),
('feeling',1,'楽[らく]に なりました','That feels better.','😌'),
('feeling',1,'助[たす]かりました','That really helped.','🙏'),
('feeling',2,'恥[は]ずかしいです','I feel embarrassed.','😳'),
('feeling',2,'ちょっと 怖[こわ]いです','I am a little scared.','😟'),
('greet',1,'お願[ねが]いします','Please.','🙇'),
('greet',1,'ありがとうございました','Thank you very much.','🙏'),
('trouble',2,'体[からだ]が 痛[いた]いです','My body hurts.','😣'),
('trouble',3,'息[いき]が 苦[くる]しいです','It is hard to breathe.','😮‍💨'),
('trouble',3,'ずれて 落[お]ちそうです','I am slipping and might fall.','⚠️'),
('trouble',3,'痰[たん]を 取[と]って ください','Please clear my phlegm.','⚠️'),
('trouble',3,'トイレに 間[ま]に合[あ]いません','I cannot make it to the toilet.','🚻'),
('trouble',2,'頭[あたま]が ぼーっと します','My head feels foggy.','😵'),
('again',1,'もう一度[いちど] お願[ねが]いします','Once more, please.','🔁'),
('again',2,'ゆっくり 言[い]って ください','Please say it slowly.','🐢'),
('again',2,'わかりませんでした','I did not understand.','❓'),
],
'test':[
('request',2,'別[べつ]の 部屋[へや]で 受[う]けたいです','I would like to take the test in a separate room.','🚪'),
('request',2,'時間[じかん]を のばして ください','Please give me extra time.','⏳'),
('request',2,'問題[もんだい]を 読[よ]み上[あ]げて ください','Please read the questions aloud.','🗣️'),
('request',2,'文字[もじ]を 大[おお]きく して ください','Please make the text larger.','🔍'),
('request',2,'パソコンで 答[こた]えたいです','I would like to answer on a computer.','💻'),
('request',2,'代[か]わりに 書[か]いて ください','Please write the answers for me.','✍️'),
('request',1,'休憩[きゅうけい]を ください','May I take a break?','☕'),
('tell',1,'終[お]わりました','I am finished.','✅'),
('tell',1,'名前[なまえ]を 書[か]きました','I wrote my name.','📝'),
('tell',1,'勉強[べんきょう]して きました','I studied for it.','📚'),
('tell',2,'この 問題[もんだい]は 飛[と]ばします','I will skip this question.','⏭️'),
('question',1,'あと 何分[なんぷん]ですか','How many minutes are left?','⏱️'),
('question',2,'何[なに]を 使[つか]っても いいですか','What am I allowed to use?','✏️'),
('question',1,'見直[みなお]しても いいですか','May I check my answers?','🔍'),
('question',2,'結果[けっか]は いつ わかりますか','When will we get the results?','📊'),
('refuse',3,'今日[きょう]は 受[う]けられません','I cannot take the test today.','🙅'),
('refuse',1,'読[よ]み上[あ]げは 要[い]りません','I do not need it read aloud.','👌'),
('refuse',1,'手伝[てつだ]いは 要[い]りません','I do not need help.','👌'),
('feeling',2,'緊張[きんちょう]しています','I am nervous.','😬'),
('feeling',1,'できました、 うれしいです','I did it. I am happy.','😊'),
('feeling',2,'くやしいです','I am frustrated.','😤'),
('feeling',3,'頭[あたま]が 真[ま]っ白[しろ]です','My mind has gone blank.','😶'),
('greet',1,'よろしく お願[ねが]いします','Thank you in advance.','🙇'),
('greet',1,'ありがとうございました','Thank you very much.','🙏'),
('trouble',1,'鉛筆[えんぴつ]を 落[お]としました','I dropped my pencil.','✏️'),
('trouble',1,'消[け]しゴムが ありません','I do not have an eraser.','🧽'),
('trouble',2,'問題[もんだい]の 意味[いみ]が わかりません','I do not understand the question.','❓'),
('trouble',2,'時間[じかん]が 足[た]りません','I do not have enough time.','⏳'),
('trouble',3,'気分[きぶん]が 悪[わる]いです','I feel sick.','🤢'),
('again',2,'もう一度[いちど] 説明[せつめい]して ください','Please explain again.','🔁'),
('again',2,'今[いま]の 指示[しじ]を 書[か]いて ください','Please write down that instruction.','📝'),
('again',1,'もう一度[いちど] 読[よ]んで ください','Please read it again.','🔁'),
],
'duty':[
('request',2,'やり方[かた]を 教[おし]えて ください','Please show me how to do it.','👀'),
('request',1,'いっしょに やって ください','Please do it with me.','🤝'),
('request',2,'重[おも]いので 手伝[てつだ]って ください','It is heavy. Please help me.','📦'),
('request',2,'できる 係[かかり]に して ください','Please give me a job I can do.','🙋'),
('tell',1,'今日[きょう]は わたしの 当番[とうばん]です','I am on duty today.','📋'),
('tell',1,'終[お]わりました','I am done.','✅'),
('tell',1,'配[くば]ります','I will hand them out.','📄'),
('tell',1,'黒板[こくばん]を 消[け]しました','I cleaned the blackboard.','🧽'),
('question',1,'今日[きょう]の 当番[とうばん]は だれですか','Who is on duty today?','❓'),
('question',2,'何[なに]を すれば いいですか','What should I do?','❓'),
('question',1,'どこに 片付[かたづ]けますか','Where do I put this away?','📦'),
('refuse',2,'それは 重[おも]くて 持[も]てません','That is too heavy for me.','🙅'),
('refuse',2,'今日[きょう]は 代[か]わって ほしいです','Could someone take my turn today?','🔄'),
('feeling',1,'係[かかり]の 仕事[しごと]が 楽[たの]しいです','I enjoy my class job.','😊'),
('feeling',1,'うまく できて うれしいです','I am happy I did it well.','😊'),
('feeling',2,'一人[ひとり]で 心配[しんぱい]です','I am worried doing it alone.','😟'),
('greet',1,'日直[にっちょく]です。 よろしく お願[ねが]いします','I am today\'s class leader. Thank you.','🙋'),
('greet',1,'起立[きりつ]、 礼[れい]','Stand up. Bow.','🙇'),
('trouble',2,'こぼして しまいました','I spilled it.','💦'),
('trouble',3,'割[わ]って しまいました','I broke it.','💥'),
('trouble',2,'忘[わす]れて いました','I forgot.','😥'),
('again',1,'もう一度[いちど] 教[おし]えて ください','Please tell me again.','🔁'),
('again',1,'順番[じゅんばん]を もう一度[いちど] お願[ねが]いします','Please tell me the order again.','🔢'),
],
'accom':[
('request',2,'授業[じゅぎょう]の 配慮[はいりょ]を 申[もう]し込[こ]みたいです','I would like to apply for accommodations.','🗂️'),
('request',2,'資料[しりょう]を 前[まえ]もって いただけますか','Could I get the materials in advance?','📄'),
('request',2,'試験[しけん]時間[じかん]の 延長[えんちょう]を お願[ねが]いしたいです','I would like extended time for exams.','⏳'),
('request',2,'ノートテイクを お願[ねが]いしたいです','I would like note-taking support.','📝'),
('request',2,'録音[ろくおん]を 許可[きょか]して ください','Please allow me to record the lecture.','🎙️'),
('request',1,'教室[きょうしつ]の 前[まえ]の 席[せき]に して ください','Please let me sit at the front.','💺'),
('tell',2,'障害[しょうがい]の ことで 相談[そうだん]が あります','I would like to talk about my disability.','💬'),
('tell',2,'診断書[しんだんしょ]を 持[も]って きました','I brought my medical certificate.','📄'),
('tell',2,'先生[せんせい]に 伝[つた]えて ほしいです','I would like you to tell my instructors.','📨'),
('tell',1,'話[はな]すのに 時間[じかん]が かかります','It takes me time to speak.','⏳'),
('question',2,'どこに 相談[そうだん]すれば いいですか','Where should I go for advice?','❓'),
('question',2,'どんな 書類[しょるい]が 必要[ひつよう]ですか','What documents do I need?','📄'),
('question',2,'いつまでに 出[だ]せば いいですか','When is the deadline?','📅'),
('question',2,'先生[せんせい]には どう 伝[つた]わりますか','How will my instructors be informed?','❓'),
('refuse',2,'今[いま]は まだ 決[き]められません','I cannot decide yet.','🤔'),
('refuse',2,'その 方法[ほうほう]は 合[あ]いません','That method does not suit me.','🙅'),
('refuse',3,'ほかの 人[ひと]には 言[い]わないで ください','Please do not tell anyone else.','🤫'),
('feeling',1,'相談[そうだん]できて 安心[あんしん]しました','I feel relieved I could talk about it.','😌'),
('feeling',2,'不安[ふあん]です','I feel anxious.','😟'),
('greet',1,'よろしく お願[ねが]いします','Thank you in advance.','🙇'),
('greet',1,'ありがとうございました','Thank you very much.','🙏'),
('trouble',3,'配慮[はいりょ]が 守[まも]られて いません','My accommodations are not being followed.','⚠️'),
('trouble',2,'授業[じゅぎょう]に ついて いけません','I cannot keep up with the class.','😥'),
('again',1,'もう一度[いちど] 説明[せつめい]して ください','Please explain again.','🔁'),
('again',2,'紙[かみ]に 書[か]いて いただけますか','Could you write it down for me?','📝'),
],
'commute':[
('request',2,'駅[えき]まで いっしょに 来[き]て ください','Please come with me to the station.','🚉'),
('request',2,'道[みち]を 教[おし]えて ください','Please tell me the way.','🗺️'),
('request',2,'迎[むか]えに 来[き]て ください','Please come and pick me up.','🚗'),
('request',1,'ゆっくり 歩[ある]いて ください','Please walk slowly.','🐢'),
('tell',1,'今[いま] 学校[がっこう]に 着[つ]きました','I just arrived at school.','🏫'),
('tell',2,'電車[でんしゃ]が 遅[おく]れて います','The train is delayed.','🚃'),
('tell',2,'少[すこ]し 遅[おく]れます','I will be a little late.','⏰'),
('tell',1,'一人[ひとり]で 帰[かえ]れます','I can go home by myself.','🚶'),
('question',1,'今日[きょう]は 何時[なんじ]に 帰[かえ]りますか','What time do I go home today?','🕒'),
('question',1,'迎[むか]えは だれが 来[き]ますか','Who is picking me up?','❓'),
('question',2,'雨[あめ]の 日[ひ]は どう しますか','What do I do on rainy days?','☔'),
('refuse',2,'一人[ひとり]で 帰[かえ]りたいです','I want to go home by myself.','🚶'),
('refuse',1,'寄[よ]り道[みち]は しません','I will not stop anywhere on the way.','🙅'),
('refuse',3,'ついて こないで ください','Please do not follow me.','✋'),
('feeling',1,'通学[つうがく]に 慣[な]れました','I have gotten used to commuting.','😊'),
('feeling',2,'満員[まんいん]電車[でんしゃ]が つらいです','Crowded trains are hard for me.','😣'),
('greet',1,'行[い]って きます','I am off.','👋'),
('greet',1,'ただいま','I am home.','🏠'),
('greet',1,'さようなら','Goodbye.','👋'),
('trouble',2,'道[みち]に 迷[まよ]いました','I am lost.','🧭'),
('trouble',2,'定期券[ていきけん]を なくしました','I lost my commuter pass.','🎫'),
('trouble',3,'知[し]らない 人[ひと]に 声[こえ]を かけられました','A stranger spoke to me.','⚠️'),
('again',1,'もう一度[いちど] 言[い]って ください','Please say that again.','🔁'),
],
'career_c':[
('request',2,'履歴書[りれきしょ]を 見[み]て ください','Please look at my résumé.','📄'),
('request',2,'面接[めんせつ]の 練習[れんしゅう]を したいです','I would like to practice for interviews.','🗣️'),
('request',2,'求人[きゅうじん]を 紹介[しょうかい]して ください','Please introduce me to job openings.','📋'),
('request',2,'障害者[しょうがいしゃ]雇用[こよう]の ことを 教[おし]えて ください','Please tell me about disability employment.','💼'),
('tell',1,'働[はたら]きたい 仕事[しごと]が あります','There is a job I want to do.','💼'),
('tell',1,'まだ 決[き]まって いません','I have not decided yet.','🤔'),
('tell',1,'説明会[せつめいかい]に 行[い]きました','I went to a company information session.','🏢'),
('question',2,'面接[めんせつ]では 何[なに]を 聞[き]かれますか','What will they ask in the interview?','❓'),
('question',2,'配慮[はいりょ]は 会社[かいしゃ]に 伝[つた]えたほうが いいですか','Should I tell the company about my accommodations?','❓'),
('question',2,'いつまでに 決[き]めれば いいですか','By when do I need to decide?','📅'),
('refuse',2,'その 仕事[しごと]は 合[あ]わないと 思[おも]います','I do not think that job suits me.','🙅'),
('refuse',3,'今日[きょう]は 面談[めんだん]を やめたいです','I would like to cancel today\'s meeting.','✋'),
('feeling',2,'不安[ふあん]です','I feel anxious.','😟'),
('feeling',1,'内定[ないてい]が もらえて うれしいです','I am happy I got a job offer.','🎉'),
('greet',1,'よろしく お願[ねが]いします','Thank you in advance.','🙇'),
('greet',1,'お時間[じかん] ありがとうございました','Thank you for your time.','🙏'),
('trouble',2,'何[なに]から 始[はじ]めれば いいか わかりません','I do not know where to start.','😥'),
('again',1,'もう一度[いちど] 説明[せつめい]して ください','Please explain again.','🔁'),
('again',2,'メールでも 送[おく]って いただけますか','Could you also send it by email?','📧'),
],
'picnic':[
('request',1,'レジャーシートを 敷[し]いて ください','Please spread out the picnic sheet.','🧺'),
('request',2,'日陰[ひかげ]で 食[た]べたいです','I would like to eat in the shade.','🌳'),
('request',1,'お弁当[べんとう]の ふたを 開[あ]けて ください','Please open my lunch box.','🍱'),
('request',1,'手[て]を ふく ものを ください','May I have something to wipe my hands?','🧻'),
('request',1,'写真[しゃしん]を 撮[と]って ください','Please take a picture.','📷'),
('tell',1,'桜[さくら]が きれいです','The cherry blossoms are beautiful.','🌸'),
('tell',1,'お弁当[べんとう]を 持[も]って きました','I brought my lunch.','🍱'),
('tell',1,'ゴミは 持[も]って 帰[かえ]ります','I will take my trash home.','🗑️'),
('question',1,'どこで 食[た]べますか','Where are we eating?','📍'),
('question',2,'トイレは どこですか','Where is the toilet?','🚻'),
('question',1,'何時[なんじ]に 出発[しゅっぱつ]しますか','What time do we leave?','🕒'),
('question',1,'いっしょに 食[た]べても いいですか','May I eat with you?','🤝'),
('refuse',2,'虫[むし]が いるので 移[うつ]りたいです','There are bugs. I want to move.','🐜'),
('refuse',2,'ここは まぶしいです','It is too bright here.','☀️'),
('feeling',1,'外[そと]で 食[た]べると おいしいです','Food tastes good outside.','😋'),
('feeling',1,'風[かぜ]が 気持[きも]ちいいです','The breeze feels nice.','🍃'),
('feeling',2,'暑[あつ]くて 疲[つか]れました','I am tired from the heat.','🥵'),
('greet',1,'いただきます','Let\'s eat.','🙏'),
('greet',1,'ごちそうさまでした','Thank you for the meal.','🙏'),
('trouble',2,'飲[の]み物[もの]が なくなりました','I ran out of my drink.','🥤'),
('trouble',2,'虫[むし]に 刺[さ]されました','I got a bug bite.','🦟'),
('trouble',3,'気分[きぶん]が 悪[わる]いです','I feel sick.','🤢'),
('again',1,'もう一度[いちど] 言[い]って ください','Please say that again.','🔁'),
],
}

# ---- 場面の定義 ----
def S(id,ruby,en,icon): return {'id':id,'ruby':ruby,'hira':hira(ruby),'kanji':kanji(ruby),'en':en,'icon':icon}
SC={
 'class':S('class','授業[じゅぎょう]','In class','📖'),
 'lecture':S('lecture','講義[こうぎ]','Lecture','🧑‍🏫'),
 'break':S('break','休[やす]み時間[じかん]','Break time','⏰'),
 'play':S('play','休[やす]み時間[じかん]・遊[あそ]び','Break / play','⚽'),
 'cbreak':S('break','休[やす]み時間[じかん]・友[とも]だち','Break / friends','☕'),
 'lunch':S('lunch','昼[ひる]ごはん','Lunch','🍱'),
 'move':S('move','移動[いどう]','Moving around','🚶'),
 'nurse':S('nurse','保健室[ほけんしつ]','Nurse\'s office','🩹'),
 'support':S('support','保健室[ほけんしつ]・学生[がくせい]相談[そうだん]','Health center / student counseling','🩺'),
 'event':S('event','行事[ぎょうじ]','School events','🎉'),
 'circle':S('circle','行事[ぎょうじ]・サークル','Events / clubs','🎪'),
 'afterschool':S('afterschool','放課後[ほうかご]','After school','🌇'),
 'commute_e':S('commute','登下校[とうげこう]・放課後[ほうかご]','Going to and from school / after school','🚸'),
 'commute':S('commute','登下校[とうげこう]・通学[つうがく]','Going to and from school','🚸'),
 'commute_c':S('commute','移動[いどう]・通学[つうがく]','Getting around / commuting','🚃'),
 'bus':S('bus','スクールバス','School bus','🚌'),
 'care':S('care','介助[かいじょ]・体[からだ]のこと','Care / my body','🤲'),
 'duty':S('duty','当番[とうばん]・係[かかり]','Class duties','🧹'),
 'club':S('club','部活[ぶかつ]','Club activities','🏀'),
 'test':S('test','テスト','Tests','📝'),
 'career':S('career','進路[しんろ]・面談[めんだん]','Future plans / meetings','🧭'),
 'career_c':S('career','就職[しゅうしょく]活動[かつどう]','Job hunting','🧭'),
 'practice':S('practice','実習[じっしゅう]','Work practice','🛠️'),
 'practice_j':S('practice','職場[しょくば]体験[たいけん]','Work experience','🛠️'),
 'seminar':S('seminar','実習[じっしゅう]・ゼミ','Practicum / seminar','🔬'),
 'office':S('office','履修[りしゅう]・事務[じむ]窓口[まどぐち]','Course registration / admin office','🏢'),
 'accom':S('accom','配慮[はいりょ]の 申[もう]し出[で]','Requesting accommodations','🗂️'),
}
# 立場ごとの場面の並び（共通 → 特有）。値は (場面キー, 表現の出どころ)
PLAN={
 'elementary':['class','play','lunch','move','nurse','event','commute_e','bus','care','duty'],
 'juniorhigh':['class','break','lunch','move','nurse','event','afterschool','commute','bus','care','duty','club','test','career','practice_j'],
 'highschool':['class','break','lunch','move','nurse','event','afterschool','commute','bus','care','club','test','career','practice','office'],
 'college':['lecture','cbreak','lunch','commute_c','support','circle','bus','care','test','career_c','seminar','office','accom'],
}
HIDDEN_DEFAULT={'highschool':['office']}   # 一部の高校だけ（単位制・通信制）。設定で出せる
LUNCH_DEFAULT={'elementary':'kyushoku','juniorhigh':'kyushoku','highschool':'bento','college':'gakushoku'}

E=d['expressions']
old=lambda role,scene:[e for e in E if e['role']==role and e['scene']==scene]
def fresh(role,scene,items,sub=''):
    out=[]
    for i,(it,lv,rb,en,ic) in enumerate(items,1):
        out.append({'id':f'{role}_{scene}{("_"+sub) if sub else ""}_{it}_{i:02d}','role':role,'scene':scene,'intent':it,'level':lv,
                    'hira':hira(rb),'kanji':kanji(rb),'ruby':rb,'en':en,'icon':ic,**({'sub':sub} if sub else {})})
    return out
def copyto(rows,role,scene,sub=''):
    out=[]
    for k,e in enumerate(rows,1):
        n=dict(e); n['role']=role; n['scene']=scene; n['id']=f'{role}_{scene}{("_"+sub) if sub else ""}_{e["intent"]}_c{k:03d}'
        if sub: n['sub']=sub
        out.append(n)
    return out

# 昼ごはんの5つの形（出どころ）
LUNCH_POOL={
 'kyushoku':lambda role: old('elementary','lunch') if role=='elementary' else old('juniorhigh','lunch'),
 'bento':lambda role: old('highschool','lunch'),
 'gakushoku':lambda role: old('college','cafeteria'),
 'gaishoku':lambda role: old('shopping','order')+old('shopping','dining'),
 'picnic':None,
}
# 既存の表現の出どころ
SRC_MAP={
 ('juniorhigh','career'):('juniorhigh','consult'),
 ('juniorhigh','practice'):('highschool','practice'),
 ('highschool','club'):('juniorhigh','club'),
 ('highschool','office'):('college','office'),
}
newE=[e for e in E if e['role'] not in PLAN]
scenes=[s for s in d['scenes'] if s['role'] not in PLAN]
added=0
for role,keys in PLAN.items():
    for key in keys:
        sc=dict(SC[key]); sc['role']=role; sid=sc['id']; scenes.append(sc)
        if sid=='lunch':
            for sub,f in LUNCH_POOL.items():
                if f: newE+=copyto(f(role),role,'lunch',sub)
                else: newE+=fresh(role,'lunch',NEW['picnic'],sub); added+=len(NEW['picnic'])
            continue
        nk={'career_c':'career_c'}.get(key,sid)
        if key=='commute_c': newE+=old(role,'commute'); continue
        if key=='commute_e': newE+=old(role,'commute'); continue
        if nk in NEW and not old(role,sid) and (role,sid) not in SRC_MAP:
            newE+=fresh(role,sid,NEW[nk]); added+=len(NEW[nk]); continue
        if (role,sid) in SRC_MAP:
            r2,s2=SRC_MAP[(role,sid)]; newE+=copyto(old(r2,s2),role,sid); continue
        rows=old(role,sid)
        if not rows: raise SystemExit(f'no source for {role}/{sid}')
        newE+=rows
d2=dict(d); d2['version']='0.5'; d2['built']='20261014'; d2['scenes']=scenes; d2['expressions']=newE
d2['lunchKinds']=[
 {'id':'kyushoku','ruby':'給食[きゅうしょく]','en':'School lunch'},
 {'id':'bento','ruby':'お弁当[べんとう]','en':'Packed lunch'},
 {'id':'gakushoku','ruby':'学食[がくしょく]・購買[こうばい]','en':'Cafeteria / store'},
 {'id':'gaishoku','ruby':'外食[がいしょく]','en':'Eating out'},
 {'id':'picnic','ruby':'ピクニック・遠足[えんそく]','en':'Picnic / field trip'}]
for k in d2['lunchKinds']: k['hira']=hira(k['ruby']); k['kanji']=kanji(k['ruby'])
d2['lunchDefault']=LUNCH_DEFAULT; d2['hiddenDefault']=HIDDEN_DEFAULT
ids=[e['id'] for e in newE]; assert len(ids)==len(set(ids)),'dup id'
json.dump(d2,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
# 新しく書いた表現のレビュー用CSV
with open('kotomusubi_public_dict-review_v0.5_20261014.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['場面','意図','強さ','漢字かな','ふりがな付き','ひらがな','English','直したほうがよい点'])
    seen=set()
    for k,items in NEW.items():
        for it,lv,rb,en,ic in items:
            if (k,rb) in seen: continue
            seen.add((k,rb)); w.writerow([k,it,lv,kanji(rb),rb,hira(rb),en,''])
import collections
print('expressions',len(E),'->',len(newE),'new written',sum(len(v) for v in NEW.values()))
for role in PLAN: print(role,collections.Counter(e['scene'] for e in newE if e['role']==role))
