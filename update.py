import sqlite3
import requests

# Crete db if it doesn't exist
with sqlite3.connect('tradingview.db') as con:
    db = con.cursor()
    db.execute(
        "CREATE TABLE IF NOT EXISTS tv (screener TEXT, exchange TEXT, symbol TEXT, desc TEXT)")
    con.commit()

# Delete all rows
with sqlite3.connect('tradingview.db') as con:
    db = con.cursor()
    db.execute("DELETE FROM tv")
    con.commit()

screener = ["america", "forex", "crypto", "indonesia", "india", "cfd", "uk", "brazil", "vietnam", "rsa", "ksa",
            "australia", "russia", "thailand", "philippines", "taiwan", "sweden", "france", "turkey", "euronext", "germany", "spain"]

for types in ["", "\"futures\""]:
    for x in screener:
        print(f"Loading screener: {x}")
        r = requests.post(f"https://scanner.tradingview.com/{x}/scan",
                          data=f'{{"symbols":{{"tickers":[],"query":{{"types":[{types}]}}}},"columns":["description"]}}')
        data = []
        for res in r.json()["data"]:
            exchange, symbol = res["s"].split(":")
            desc = res["d"][0]
            data.append((x, exchange, symbol, desc,))

        # Use bulk operation for faster insert
        with sqlite3.connect('tradingview.db') as con:
            con.executemany(
                "INSERT INTO tv VALUES (?, ?, ?, ?)",
                data
            )
