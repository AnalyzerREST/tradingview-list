from flask import Flask, render_template, request, jsonify
import sqlite3

# db = sqlite3.connect('tradingview.db').cursor()
# db.execute("CREATE TABLE tv (screener, exchange, symbol, desc)")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    screener = request.args.get("sc", default='all')
    q = f"%{request.args['q']}%"
    with sqlite3.connect("tradingview.db") as con:
        db = con.cursor()
        if screener == "all":
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE exchange LIKE ? OR symbol LIKE ? OR desc LIKE ? LIMIT 10", (q, q, q))
        else:
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE screener = ? AND (exchange LIKE ? OR symbol LIKE ? OR desc LIKE ?) LIMIT 10", (screener, q, q, q))
    return jsonify({"r": list(rows)})

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')