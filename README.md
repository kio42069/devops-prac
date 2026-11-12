# System Monitor

A small local dashboard for CPU and memory usage. The browser updates every 5 seconds. The server saves samples in SQLite and keeps the last 24 hours.

## Run it

From the `app` folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Open <http://127.0.0.1:5000>. Stop with Ctrl+C. The dashboard monitors the computer running `server.py`.

## Where things are

| File | Purpose |
| --- | --- |
| `server.py` | Reads system stats, serves the page and `/api/stats`, stores samples |
| `templates/index.html` | Dashboard layout |
| `static/app.js` | Fetches stats and updates the page |
| `static/style.css` | Colors and layout |
| `stats.db` | SQLite history, created automatically when the page first fetches stats |

## Add a feature

1. Read the new value with `psutil` in `server.py` and add it to the JSON returned by `stats()`.
2. Add a place to display it in `templates/index.html`.
3. Update that element in `static/app.js`; adjust `static/style.css` if needed.

For example, disk usage can come from `psutil.disk_usage('/').percent`. To keep a new value in history, also add a column to the `samples` table and update its insert and select queries. For an existing `stats.db`, either migrate the table or delete the database to start fresh.
