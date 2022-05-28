import sqlite3, requests

with sqlite3.connect('tradingview.db') as con:
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS tv (screener TEXT, exchange TEXT, symbol TEXT, desc TEXT)")
    con.commit()

screener = ["america", "forex", "crypto", "indonesia", "india", "cfd", "uk", "brazil", "vietnam", "rsa", "ksa", "australia", "russia", "thailand", "philippines", "taiwan", "sweden", "france", "turkey"]

def add(screener, exchange, symbol, description):
    with sqlite3.connect('tradingview.db') as con:
        db = con.cursor()
        db.execute("INSERT INTO tv SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM tv WHERE screener = ? AND exchange = ? AND symbol = ?)", (screener, exchange, symbol, description, screener, exchange, symbol))
        con.commit()

for x in screener:
    r = requests.post(f"https://scanner.tradingview.com/{x}/scan", data='{"symbols":{"tickers":[],"query":{"types":[]}},"columns":["description"]}')
    for res in r.json()["data"]:
        exchange, symbol = res["s"].split(":")
        desc = res["d"][0]
        add(x, exchange, symbol, desc)
