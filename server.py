from pathlib import Path
import sqlite3
import time

from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)
DB = Path(__file__).with_name("stats.db")


def database():
    connection = sqlite3.connect(DB)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS samples (time INTEGER PRIMARY KEY, cpu REAL, ram REAL)"
    )
    return connection


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/stats")
def stats():
    now = int(time.time())
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    with database() as db:
        db.execute("INSERT OR REPLACE INTO samples VALUES (?, ?, ?)", (now, cpu, memory.percent))
        db.execute("DELETE FROM samples WHERE time < ?", (now - 86400,))
        history = db.execute(
            "SELECT time, cpu, ram FROM samples ORDER BY time DESC LIMIT 30"
        ).fetchall()
    return jsonify({
        "cpu": cpu,
        "ram": memory.percent,
        "ram_used_gb": round(memory.used / 1024**3, 1),
        "ram_total_gb": round(memory.total / 1024**3, 1),
        "history": [dict(time=t, cpu=c, ram=r) for t, c, r in reversed(history)],
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
