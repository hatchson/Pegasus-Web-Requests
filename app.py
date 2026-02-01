from flask import Flask, render_template, jsonify, request, abort
import sqlite3

app = Flask(__name__)
DB = "pegasus.db"
API_KEY = "SUPER_SECRET_KEY_CHANGE_ME"  # put same key in bot

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS admins (id TEXT PRIMARY KEY, added_by TEXT)")

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/check/<admin_id>")
def check_admin(admin_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT 1 FROM admins WHERE id=?", (admin_id,))
        if cur.fetchone():
            return jsonify({"status": "Success"})
    return jsonify({"status": "Denied"})

@app.route("/api/add", methods=["POST"])
def add_admin():
    if request.headers.get("Authorization") != API_KEY:
        abort(403)
    data = request.json
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT OR IGNORE INTO admins (id, added_by) VALUES (?, ?)",
                     (data["id"], data["added_by"]))
    return jsonify({"result": "added"})

@app.route("/api/delete", methods=["POST"])
def delete_admin():
    if request.headers.get("Authorization") != API_KEY:
        abort(403)
    data = request.json
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM admins WHERE id=?", (data["id"],))
    return jsonify({"result": "deleted"})
