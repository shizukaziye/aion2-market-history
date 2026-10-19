# Aion 2 market history: Korea vs Taiwan vs Global

Dated Kina prices of Aion 2 crafting materials on the Korean and Taiwanese servers (quoted from DCInside, Inven and Bahamut posts, source linked on every point) against the global servers (daily medians of the cheapest ask on aion2.exchange), on a weeks-since-launch axis. One tab per item.

Live: https://shizukaziye.github.io/aion2-market-history/

- `tools/pull_global.py <out.json>` pulls the global daily series (six servers) from aion2.exchange.
- `tools/build_data.py` holds the hand-transcribed KR/TW points and writes `data.js`.
- No build step, no dependencies; `index.html` + `styles.css` + `app.js` + `data.js`.
