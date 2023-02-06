from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sqlite3
import json
import zlib
import config
import os

app = Flask(__name__)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
ad = os.environ.get("AD_CODE")


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html", screener=sorted(config.SCREENER.items(), key=lambda x: x[1]), ad=ad)


@socketio.on("search_event")
def handle_search_event(data):
    screener = data["screener"]
    query = data["query"]
    page = data["page"]
    q = f"%{query}%"
    with sqlite3.connect("tradingview.db") as con:
        db = con.cursor()
        if screener == "all":
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE exchange LIKE ? OR symbol LIKE ? OR desc LIKE ? LIMIT ? OFFSET ?",
                              (q, q, q, config.PAGE_SIZE, (page - 1) * config.PAGE_SIZE))
        else:
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE screener = ? AND (exchange LIKE ? OR symbol LIKE ? OR desc LIKE ?) LIMIT ? OFFSET ?",
                              (screener, q, q, q, config.PAGE_SIZE, (page - 1) * config.PAGE_SIZE))
    emit('response', {"r": zlib.compress(
        bytes(json.dumps(list(rows)), "utf-8"))})


if __name__ == '__main__':
    print("Starting server: http://localhost:5000")
    socketio.run(app, debug=False)
