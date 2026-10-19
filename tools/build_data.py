"""Build data.js for the Aion 2 market-history page.

Sources:
  data/global_series.json  - aion2.exchange daily medians (tools/pull_global.py)
  the KR / TW point lists below - hand-transcribed from DCInside aion2 gallery, Inven and Bahamut
    (post numbers in `src` are DCInside https://gall.dcinside.com/mgallery/board/view/?id=aion2&no=<n>
     unless the entry carries a full URL)

Usage: python -I -X utf8 tools/build_data.py
"""
import json, os, statistics
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCH = {"KR": date(2025, 11, 19), "TW": date(2025, 11, 19), "GL": date(2026, 10, 5)}
DC = "https://gall.dcinside.com/mgallery/board/view/?id=aion2&no="
BAHA = "https://forum.gamer.com.tw/C.php?bsn=82913&snA="

def P(d, price, conf, src, quote, note=""):
    y, m, dd = [int(x) for x in d.split("-")]
    return {"date": d, "price": price, "conf": conf, "src": (DC + src if src.isdigit() else src), "quote": quote, "note": note}

ICON = "https://gamers4.life/aion-2/database/icons/assets/Game/UI/Resource/Texture/Item/"

ITEMS = [
 {"key": "610511013", "name": "Wrathful Mind", "kr": "분노의 사념", "tw": "憤怒思念", "icon": ICON + "ETC/Icon_Item_Material_Craft_Draconic_L_lv1_04.webp",
  "about": "Tier-1 wrath material (Krao Cave, Draupnir). Only drops where nobody geared farms, so the price follows how many alts still run T1.",
  "KR": [
   P("2025-11-26", 1150000, "quoted", "https://www.inven.co.kr/board/aion2/6388/17208", "시엘서버는 100~130만임 / Siel server 1.0-1.3M", "Zenkaka 670k the same day"),
   P("2025-12-16", 1400000, "quoted", "790887", "제작재료 사념 25만 > 140만 / Mind 250k to 1.4M", "blamed on the drop-rate change"),
   P("2025-12-30", 2000000, "quoted", "968395", "돌파석 15 사념 200쯤 / Amp 150k, Mind ~2.0M, same both factions"),
   P("2026-01-17", 2500000, "rough", "1212982", "250 고점찍고 / peaked at 2.5M", "date of the peak inferred from the Jan 19 post"),
   P("2026-01-19", 1990000, "quoted", "1212982", "199만까지 추락 / crashed to 1.99M"),
   P("2026-02-11", 1500000, "rough", "1542110", "찬오드 사념 의지도 떡락 / Radiant Odyle, Mind and Will all crashed", "no number given; T4 dungeons started dropping Mind and Will"),
   P("2026-03-16", 3000000, "quoted", "1865536", "300만이나한다고 / it costs 3M", "alts left Krao for Fire Temple (free Arcana), supply died"),
   P("2026-04-20", 1800000, "quoted", "2221858", "사념은 180만키나 / Mind 1.8M"),
   P("2026-07-25", 5000000, "rough", "2745871", "사념의지가 500임 / Mind and Will at 5M", "party-recruit title; 2989759 on Sep 28 remembers the 5M days"),
   P("2026-10-01", 300000, "quoted", "3003098", "분노의사념 30만원대 / Mind in the 300k range", "upper-tier dungeons now drop it tradeable"),
  ],
  "TW": [
   P("2026-01-12", None, "rough", BAHA + "3489", "龍王裝和製作素材的價格倒是平盤穩定 / dragon-king gear and crafting materials flat", "no number"),
   P("2026-02-10", None, "rough", BAHA + "4049", "現在龍材都1.5~2倍再漲價 / dragon materials up 1.5x to 2x", "no number"),
   P("2026-02-06", None, "rough", BAHA + "4009", "材料貴到一個可怕 / materials terrifyingly expensive", "no number"),
  ]},
 {"key": "610511014", "name": "Wrathful Will", "kr": "분노의 의지", "tw": "憤怒意志", "icon": ICON + "ETC/Icon_Item_Material_Craft_Draconic_L_lv2_04.webp",
  "about": "Tier-2 wrath material (Urugugu Canyon, Vakron Sky Island). Tracked Mind on Korea and overtook it at the summer peak.",
  "KR": [
   P("2026-01-20", 1500000, "rough", "1237876", "사념 의지 자아 가격 똑같아짐 / Mind, Will and Ego prices became the same", "Ego was 1.05M and Mind 1.99M that day; midpoint used"),
   P("2026-02-11", 1000000, "rough", "1538180", "사념 의지 4티어에서 나와서 수요 이동 / Mind and Will now drop in T4, demand moved on", "no number"),
   P("2026-07-23", 6000000, "quoted", "2740257", "의지 600만 ㅋㅋㅋ / Will 6M"),
   P("2026-10-19", None, "rough", "https://gall.dcinside.com/mgallery/board/lists/?id=aion2&s_type=search_subject_memo&s_keyword=%EC%82%AC%EB%85%90", "의지 사념 챕터2에서 고트온다 / Will and Mind are the GOAT again in Chapter 2", "no number"),
  ],
  "TW": [P("2026-02-10", None, "rough", BAHA + "4049", "龍材都1.5~2倍再漲價 / dragon materials up 1.5x to 2x", "no number")]},
 {"key": "610511015", "name": "Wrathful Ego", "kr": "분노의 자아", "tw": "憤怒自我", "icon": ICON + "ETC/Icon_Item_Material_Craft_Draconic_L_lv3_04.webp",
  "about": "Tier-3 wrath material (Fire Temple, Ferocious Horn Den). The whole server farms T3, so Korea's Ego lagged Mind and Will all year.",
  "KR": [
   P("2026-01-05", 500000, "rough", "1118226", "자아 50정도였는데 / Ego was about 500k", "the 'before' value in a Jan 11 post"),
   P("2026-01-11", 1000000, "rough", "1118759", "월드 거래소 기준 100만이 멀지 않았네 / nearly 1M on the World Market"),
   P("2026-01-20", 1050000, "quoted", "1241006", "자아 왜 105만원 / why is Ego 1.05M", "players stuck at Fire Temple made Ego the bottleneck (1237862)"),
   P("2026-04-20", None, "rough", "2223541", "분노의자아 떡상할거같은데 / Ego looks about to moon", "no number"),
   P("2026-07-20", 800000, "quoted", "2718807", "자아 조차도 80만원 대임 / even Ego is in the 800k range"),
  ],
  "TW": []},
 {"key": "516530001", "name": "Amplify Stone (Unique)", "kr": "유일 돌파석", "tw": "突破石", "icon": "",
  "about": "The Amp (breakthrough) stone. Korea sat at 100k to 240k through its first four months; global is a third of that.",
  "KR": [
   P("2025-12-15", 110000, "quoted", "781963", "11만이엇는데 / it was 110k", "then jumped; blamed on a whale"),
   P("2025-12-25", 110000, "quoted", "919080", "돌파석 11만에 던지는거 / dumping Amp stones at 110k", "daily dungeon fixed, stones crashing (917319)"),
   P("2025-12-30", 150000, "quoted", "968395", "돌파석 15 / Amp stone 150k"),
   P("2026-01-20", 120000, "quoted", "1239585", "아침에 돌파석 12에 다 털었는데 / sold all at 120k in the morning"),
   P("2026-01-20", 240000, "quoted", "1239737", "돌파석 24만대에 100개정도 정리 / sold ~100 in the 240k range", "same day: bracelet pity rush; 'sell at 100k, buy at 200k' (1239507)"),
   P("2026-02-11", 90000, "rough", "1538281", "유일 돌파석 나락가서 / Unique Amp stones went to the gutter", "no number"),
   P("2026-03-18", 85000, "quoted", "1889523", "돌파석 8만원대에 풀매수 / bought the book at 80k-something", "armor Amp announced, buyers expected a rise"),
  ],
  "TW": [P("2026-01-01", None, "rough", BAHA + "3303", "一顆突破石約10萬基納的強化石 / one Amp stone costs about 100k of enhance stones to make", "cost estimate, not a market price")]},
 {"key": "610530008", "name": "Artisan's Refining Stone", "kr": "달인의 제련석", "tw": "達人提煉石", "icon": ICON + "ETC/Icon_Item_Craft_SmeltStone_Equip_A_e_001.webp",
  "about": "Two per Artisan's-tier craft. Korea doubled it mid-year when the Brooch recipes arrived.",
  "KR": [
   P("2026-01-20", 1000000, "rough", "1239445", "달제 100만 거의 찍어 가네 / Artisan's stone nearly hit 1M"),
   P("2026-06-01", 450000, "rough", "2718807", "제련석은 4~50만원에서 / refining stones from 400-500k", "the 'before' value in the Jul 20 post"),
   P("2026-07-20", 800000, "quoted", "2718807", "80만원대 / 800k range", "blue Brooch demand"),
  ],
  "TW": [P("2026-09-28", None, "rough", BAHA + "6240", "達人最上級提煉石 打不到幾顆 / can barely get any Artisan's Ultimate stones", "scarcity, no number")]},
 {"key": "610530010", "name": "Artisan's Ultimate Refining Stone", "kr": "달인의 최상급 제련석", "tw": "達人最上級提煉石", "icon": ICON + "ETC/Icon_Item_Craft_SmeltStone_Equip_A_e_002.webp",
  "about": "The Dragon Lord tier refining stone. Korea tripled it in one night in January.",
  "KR": [
   P("2026-01-19", 380000, "quoted", "1241253", "달인의 최상급 38만->83만 / 380k to 830k", "the 'before' value"),
   P("2026-01-21", 830000, "quoted", "1241253", "달인의 최상급 38만->83만 / tripled overnight after the live broadcast"),
  ],
  "TW": [P("2026-09-28", None, "rough", BAHA + "6240", "達人最上級提煉石 製作材料依然非常缺乏 / still very scarce", "no number")]},
 {"key": "610530005", "name": "Expert's Refining Stone", "kr": "전문가의 제련석", "tw": "專家提煉石", "icon": ICON + "ETC/Icon_Item_Craft_SmeltStone_Equip_A_u_001.webp",
  "about": "Two per Expert's-tier craft. Global only; no Korean prints found.", "KR": [], "TW": []},
 {"key": "610610016", "name": "Radiant Odyle", "kr": "찬란한 오드", "tw": "燦爛的奧德", "icon": ICON + "ETC/Icon_Item_Gather_Od_A_u_001.webp",
  "about": "Rare gathering drop, in every Dragon Lord recipe and in wings. Korea held 400k to 600k for eight months; supply from gatherers caps it.",
  "KR": [
   P("2025-12-30", 450000, "quoted", "982332", "어제찬오드값45만 / Radiant Odyle was 450k yesterday"),
   P("2025-12-31", 460000, "quoted", "990970", "찬오드10개 460 / 10 Radiant Odyle for 4.6M", "same day quotes of 400k and 600k"),
   P("2026-01-20", 430000, "quoted", "1238865", "오전에 42~43에삿다 지금 51 / bought at 420-430k in the morning, 510k now"),
   P("2026-02-11", 550000, "rough", "1541720", "찬오드랑 광석 떡상 / Radiant Odyle and ore soared", "everyone crafting Heroic wings; no number"),
   P("2026-06-01", 600000, "rough", "2718807", "오드는 60 -> 40만 / Odyle 600k to 400k", "the 'before' value"),
   P("2026-07-20", 400000, "quoted", "2718807", "오드는 60 -> 40만 키나 됐고 / Odyle became 400k"),
  ],
  "TW": [P("2026-05-27", 330000, "quoted", BAHA + "5370", "之前金奧德33萬囤的 / stockpiled gold Odyle at 330k earlier", "'gold Odyle' is probably this tier; purchase date not given")]},
 {"key": "610660034", "name": "Radiant Sapphire Gemstone", "kr": "찬란한 사파이어 원석", "tw": "燦爛的藍寶石原石", "icon": ICON + "ETC/Icon_Item_Gather_Gemstone_A_u_001.webp",
  "about": "Five per Dragon Lord ring. Went from 80k to 550k on Nezekan in one week.",
  "KR": [P("2025-12-31", 500000, "quoted", "985547", "왜 찬사파를 50주고사는거냐 / why are people paying 500k for Radiant Sapphire")],
  "TW": []},
 {"key": "610730022", "name": "Enhanced Thick Balaur Scale", "kr": "강화된 두꺼운 용족의 비늘", "tw": "強化厚實的龍族鱗片", "icon": ICON + "ETC/Icon_Item_Craft_Draconic_Skin_A_r_001.webp",
  "about": "Tier-1 refined scale, 2 raw scales + hardener. Korea: expensive while people leveled crafting, ~10k on the World Market later.",
  "KR": [
   P("2025-12-31", None, "rough", "990247", "두꺼운용족의비늘 왜케 쳐비쌈 / why are Thick scales so expensive", "people leveling crafting; no number"),
   P("2026-01-01", 10000, "rough", "https://arca.live/b/aion2/157450077", "용족의 비늘류는 월드 거래소에서 1만원 안팎 / scale refines about 10k on the World Market (Asmodian)", "arca.live post, date approximate"),
  ],
  "TW": []},
 {"key": "610730023", "name": "Enhanced Hard Balaur Scale", "kr": "강화된 단단한 용족의 비늘", "tw": "強化堅硬的龍族鱗片", "icon": ICON + "ETC/Icon_Item_Craft_Draconic_Skin_A_r_002.webp",
  "about": "Tier-2 refined scale (White / Dark Dragon Lord recipes).", "KR": [], "TW": []},
 {"key": "610730024", "name": "Enhanced Durable Balaur Scale", "kr": "강화된 견고한 용족의 비늘", "tw": "強化堅固的龍族鱗片", "icon": ICON + "ETC/Icon_Item_Craft_Draconic_Skin_A_r_003.webp",
  "about": "Tier-3 refined scale (Wise / Ebony recipes); raw scales from Fire Temple and Horn Den.", "KR": [], "TW": []},
 {"key": "310330013", "name": "Artisan's Splendent Sapphire Ring", "kr": "달인의 빛나는 사파이어 반지", "tw": "達人閃耀的藍寶石戒指", "icon": ICON + "Accessory/Icon_ACC_Ring_0012.webp",
  "about": "Base piece of every crafted Dragon Lord ring. Fell from 13M to 5.5M in global week 2, back to 8-9M since.",
  "KR": [P("2026-01-20", None, "rough", "1233291", "찬오랑 제련석 달빛 액세 다 떡락 / Radiant Odyle, refining stones and Moonlight (Artisan's Splendent) accessories all crashed", "no number")],
  "TW": []},
 {"key": "310330015", "name": "True Dragon Lord Ring", "kr": "건룡왕 반지", "tw": "乾龍王戒指", "icon": ICON + "Accessory/Icon_ACC_Ring_0036.webp",
  "about": "The tradeable crafted ring (62). Korea: 'why did the True ring price jump' after the Jan 20 broadcast.",
  "KR": [P("2026-01-21", None, "rough", "1241822", "건룡반지 가격왜케오름 / why is the True ring price rising", "no number")],
  "TW": []},
 {"key": "310330017", "name": "Splendent True Dragon Lord Ring", "kr": "빛나는 건룡왕 반지", "tw": "閃耀乾龍王戒指", "icon": ICON + "Accessory/Icon_ACC_Ring_0036.webp",
  "about": "The 70 version; plain ring + a no-roll upgrade makes one.", "KR": [], "TW": []},
 {"key": "610610013", "name": "Odyle", "kr": "오드", "tw": "白奧德", "icon": ICON + "ETC/Icon_Item_Gather_Od_L_lv2_02a.webp",
  "about": "Plain gathered Odyle. Korea and Taiwan both drifted to about 10k by week 10 to 12.",
  "KR": [P("2026-02-11", 9000, "quoted", "1542701", "일반오드 가격 9000원 / regular Odyle 9,000")],
  "TW": [P("2026-01-28", 10000, "rough", BAHA + "3780", "離1萬不遠了，現在改45才能採集，繼續漲 / not far from 10k, gathering now needs level 45, still rising")]},
 {"key": "511360004", "name": "Superior Manastone", "kr": "상급 마석", "tw": "上級魔石", "icon": ICON + "ETC/Icon_Item_Usable_Enchant_MagicStone_A_c_003.webp",
  "about": "Global only. Taiwan called manastones 'futures' by June.", "KR": [], "TW": [P("2026-06-18", None, "rough", BAHA + "5466", "魔石靈石貴成這樣…玩期貨 / manastones and soulstones priced like futures", "no number")]},
 {"key": "511360003", "name": "Intermediate Manastone", "kr": "중급 마석", "tw": "中級魔石", "icon": ICON + "ETC/Icon_Item_Usable_Enchant_MagicStone_A_c_002.webp",
  "about": "Global only.", "KR": [], "TW": []},
 {"key": "602460004", "name": "Sealed Forest Spirit Wings", "kr": "봉인된 숲의 정령 날개", "tw": "封印的森林精靈翅膀", "icon": "",
  "about": "Global only; down 57% on Nezekan in week 2. Korea's wings in general were 4M to 4.9M on Dec 31 (989527, 990970).", "KR": [], "TW": []},
 {"key": "514310118", "name": "Artwork: Vakron Sky Island", "kr": "예술품: 바크론의 공중섬", "tw": "藝術品：巴克隆空中島", "icon": "",
  "about": "Global only; Nezekan is the cheapest NA East server for it.", "KR": [], "TW": []},
 {"key": "quna", "name": "Kina per Quna (exchange rate)", "kr": "큐나 환율", "tw": "奎靈 匯率", "icon": "",
  "about": "How much Kina one Quna buys through the in-game exchange. Lower = Kina is worth more. Korea's Kina devalued through the year.",
  "KR": [
   P("2026-01-20", 4444, "quoted", "1239682", "40만키나에 90큐나 / 400k Kina for 90 Quna"),
   P("2026-01-20", 4000, "quoted", "1240349", "천만키나상자 2500큐나에 20개팔림 / 10M-Kina box sold 20 times at 2,500 Quna"),
   P("2026-07-20", None, "rough", "2718807", "큐나로 키나를 안 사니까 앞으로도 6~800선으로 조일 거임 / they will keep squeezing it to the 600-800 line", "unit unclear"),
  ],
  "TW": [], "GLpoints": [P("2026-10-13", 1250, "quoted", "Shizu, Nezekan Quna exchange", "2M Kina chest = 1,600 Quna", "one listing")]},
]

def wk(region, d):
    y, m, dd = [int(x) for x in d.split("-")]
    return round((date(y, m, dd) - LAUNCH[region]).days / 7, 2)

g = json.load(open(os.path.join(ROOT, "data", "global_series.json"), encoding="utf-8"))
out = {"built": g["pulled_at"], "launch": {k: v.isoformat() for k, v in LAUNCH.items()}, "servers": g["servers"], "items": []}
for it in ITEMS:
    row = {k: it[k] for k in ("key", "name", "kr", "tw", "icon", "about")}
    for r in ("KR", "TW"):
        row[r] = [dict(p, wk=wk(r, p["date"])) for p in it[r]]
    gl = g["items"].get(it["key"])
    row["GL"] = {}
    if gl:
        for s, ser in gl["series"].items():
            row["GL"][s] = [{"date": p["d"], "wk": wk("GL", p["d"]), "price": p["med"], "min": p["min"], "listings": p["listings"]} for p in ser]
        # basket median across servers per day
        bydate = {}
        for s, ser in gl["series"].items():
            for p in ser: bydate.setdefault(p["d"], []).append(p["med"])
        row["GLavg"] = [{"date": d, "wk": wk("GL", d), "price": statistics.median(v), "n": len(v)} for d, v in sorted(bydate.items())]
    else:
        row["GLavg"] = [dict(p, wk=wk("GL", p["date"])) for p in it.get("GLpoints", [])]
    out["items"].append(row)

js = "// generated by tools/build_data.py, do not edit\nwindow.MARKET = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8").write(js)
print("items", len(out["items"]), "bytes", len(js))
