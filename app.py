from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-Memory "Datenbank" (bleibt nur solange der Server läuft)
ITEMS = [
    {"id": 1, "name": "Nägel", "qty": 5},
    {"id": 2, "name": "Schrauben", "qty": 12},
    {"id": 3, "name": "Hammer", "qty": 1},
    {"id": 4, "name": "Dübel", "qty": 20},
    {"id": 5, "name": "Säge", "qty": 2},
    {"id": 6, "name": "Zange", "qty": 1},
]

@app.route("/")
def index():
    return render_template("index.html", items=ITEMS)

@app.route("/result", methods=["GET", "POST"])
def result():
    # Falls jemand hierher kommt, zurück zur Index
    return index()

@app.route("/save", methods=["POST"])
def save():
    global ITEMS
    payload = request.get_json(force=True)
    updated = payload.get("items", [])

    # Map von id -> item
    by_id = {it["id"]: it for it in ITEMS}

    # Reihenfolge + Mengen übernehmen
    new_items = []
    for it in updated:
        _id = int(it["id"])
        qty = int(it.get("qty", 0))

        if _id in by_id:
            by_id[_id]["qty"] = qty
            new_items.append(by_id[_id])

    # Globale Liste in neuer Reihenfolge setzen
    ITEMS = new_items

    return jsonify({"ok": True, "count": len(ITEMS)})

@app.route("/data", methods=["GET"])
def data():
    # Optional: zum Debuggen
    return jsonify(ITEMS)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
