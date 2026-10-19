"""Pull Korean world-market weekly/daily series from aeid.gg's API (api-aeid.lostgld.com) into data/kr_aeid_graph.json,
and the Kina->KRW daily candles for Siel from gamebit.co.kr into data/kr_kina_krw_siel.json.
Usage: python -I -X utf8 tools/pull_kr.py
"""
import json, os, time, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://aeid.gg/", "Origin": "https://aeid.gg"}
B = "https://api-aeid.lostgld.com"
def get(u, h=UA):
    with urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=40) as r: return json.load(r)
KR = {"Wrathful Mind": "분노의 사념", "Wrathful Will": "분노의 의지", "Wrathful Ego": "분노의 자아", "Amplify Stone (Unique)": "돌파석 (유일)",
      "Amplify Stone (Heroic)": "돌파석 (영웅)", "Artisan's Refining Stone": "달인의 제련석", "Artisan's Ultimate Refining Stone": "달인의 최상급 제련석",
      "Expert's Refining Stone": "장인의 제련석", "Radiant Odyle": "찬란한 오드", "Radiant Sapphire Gemstone": "찬란한 사파이어 원석",
      "Enhanced Thick Balaur Scale": "강화된 두꺼운 용족의 비늘", "Enhanced Hard Balaur Scale": "강화된 단단한 용족의 비늘",
      "Enhanced Durable Balaur Scale": "강화된 견고한 용족의 비늘", "Artisan's Splendent Sapphire Ring": "달인의 빛나는 사파이어 반지",
      "True Dragon Lord Ring": "건룡왕의 반지", "Splendent True Dragon Lord Ring": "빛나는 건룡왕의 반지", "Odyle": "오드",
      "Superior Manastone": "상급 마석", "Intermediate Manastone": "중급 마석"}
out = {}
for en, kr in KR.items():
    rec = {"kr": kr}
    for fac in ("asmo", "elyos"):
        for per in ("week", "day"):
            try: rec[f"{fac}_{per}"] = get(f"{B}/graph-prices/{urllib.parse.quote(kr)}?faction={fac}&period={per}")
            except Exception as e: rec[f"{fac}_{per}"] = []
            time.sleep(0.15)
    out[en] = rec; print(en, len(rec["asmo_week"]), len(rec["elyos_week"]))
json.dump(out, open(os.path.join(ROOT, "data", "kr_aeid_graph.json"), "w", encoding="utf-8"), ensure_ascii=False)
try:
    k = get("https://gamebit.co.kr/v3_get_chart_data.php?game=aion&sid=21778&type=day", {"User-Agent": "Mozilla/5.0", "Referer": "https://gamebit.co.kr/aion"})
    json.dump(k, open(os.path.join(ROOT, "data", "kr_kina_krw_siel.json"), "w")); print("gamebit days", len(k))
except Exception as e: print("gamebit failed", e)
