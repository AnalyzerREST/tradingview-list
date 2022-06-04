from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")

@socketio.on("search_event")
def handle_search_event(data):
    screener = data["screener"]
    query = data["query"]
    q = f"%{query}%"
    with sqlite3.connect("tradingview.db") as con:
        db = con.cursor()
        if screener == "all":
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE exchange LIKE ? OR symbol LIKE ? OR desc LIKE ? LIMIT 20", (q, q, q))
        else:
            # https://xkcd.com/327/
            rows = db.execute("SELECT * FROM tv WHERE screener = ? AND (exchange LIKE ? OR symbol LIKE ? OR desc LIKE ?) LIMIT 20", (screener, q, q, q))
    emit('response', {"r": list(rows)})

if __name__ == '__main__':
    socketio.run(app, debug=False)