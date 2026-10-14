const CACHE="kotomusubi-0.3.5";
const SHELL=["./","manifest.webmanifest","icon.svg"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
/* 画面（HTML）は「ネット優先」：新しい版が すぐ出る。辞書などは「保存優先」：オフラインでも動く */
self.addEventListener("fetch",e=>{
  const rq=e.request; if(rq.method!=="GET") return;
  const isPage=rq.mode==="navigate"||/\.html$/.test(new URL(rq.url).pathname);
  if(isPage){
    e.respondWith(fetch(rq).then(r=>{if(r.ok){const cp=r.clone();caches.open(CACHE).then(c=>c.put(rq,cp))}return r}).catch(()=>caches.match(rq).then(h=>h||caches.match("./"))));
    return;
  }
  e.respondWith(caches.match(rq).then(hit=>{
    const net=fetch(rq).then(r=>{if(r.ok){const cp=r.clone();caches.open(CACHE).then(c=>c.put(rq,cp))}return r}).catch(()=>hit);
    return hit||net;
  }));
});
