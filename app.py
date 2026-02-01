from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "menu": "Pegasus Menu",
        "status": "In Development",
        "access_control": "Only Menu Admins can modify. Console Admins cannot.",
        "developers": ["Sudzy", "Hatchson"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

