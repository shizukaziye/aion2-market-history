import json, urllib.request, time, sys
from collections import defaultdict
UA={"User-Agent":"Mozilla/5.0 (aion2-market-history; github.com/shizukaziye)"}
EX="https://aion2.exchange/api"
def get(u):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40) as r: return json.load(r)
        except Exception as e: time.sleep(1.5*(i+1))
    return None
ITEMS={  # key: english
 "610511013":"Wrathful Mind","610511014":"Wrathful Will","610511015":"Wrathful Ego",
 "516530001":"Amplify Stone (Unique)","610530008":"Artisan's Refining Stone","610530010":"Artisan's Ultimate Refining Stone",
 "610610016":"Radiant Odyle","610660034":"Radiant Sapphire Gemstone",
 "610730022":"Enhanced Thick Balaur Scale","610730023":"Enhanced Hard Balaur Scale","610730024":"Enhanced Durable Balaur Scale",
 "310330013":"Artisan's Splendent Sapphire Ring","310330015":"True Dragon Lord Ring","310330017":"Splendent True Dragon Lord Ring",
 "610610013":"Odyle",
}
# find keys for a few more by name on Nezekan
want_names={"Expert's Refining Stone","Superior Manastone","Sealed Forest Spirit Wings","Artwork: Vakron Sky Island","Intermediate Manastone"}
items=[]; off=0
while True:
    d=get(f"{EX}/items?sort=name&order=asc&window=24h&limit=200&offset={off}&server=11102")
    items+=d['items']; off+=200
    if off>=d['total']: break
    time.sleep(0.1)
for it in items:
    if it['name'] in want_names: ITEMS[str(it['item_key'])]=it['name']
print(len(ITEMS),'items'); 
SERVERS={11102:"NAE Nezekan (Shizu)",11101:"NAE Siel",12106:"NAE Azphel (Asmodian)",12101:"NAE Israphel (Asmodian)",11304:"EU Kaisinel",12306:"EU Azphel (Asmodian)",11102+1000:"NAW?"}
SERVERS={11102:"NAE Nezekan",11101:"NAE Siel",12106:"NAE Azphel",12101:"NAE Israphel",11304:"EU Kaisinel",12306:"EU Azphel"}
out={"pulled_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"servers":SERVERS,"items":{}}
for k,name in ITEMS.items():
    out["items"][k]={"name":name,"series":{}}
    for s in SERVERS:
        d=get(f"{EX}/items/{k}/prices?server={s}&from=2026-10-01T00:00:00Z&bucket=1h")
        pts=(d or {}).get('points',[])
        day=defaultdict(list); lst=defaultdict(list)
        for p in pts:
            if p.get('low'): day[p['ts'][:10]].append(p['low']); lst[p['ts'][:10]].append(p.get('listings') or 0)
        ser=[]
        for dd in sorted(day):
            v=sorted(day[dd]); ser.append({"d":dd,"med":v[len(v)//2],"min":v[0],"listings":round(sum(lst[dd])/len(lst[dd]))})
        out["items"][k]["series"][str(s)]=ser
        time.sleep(0.1)
    print(name, {s:len(v) for s,v in out["items"][k]["series"].items()})
json.dump(out, open(sys.argv[1],'w'))
print('done')
