from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__)

# Pfad zur Excel-Datei (kann relativ zum Projektverzeichnis sein)
EXCEL_FILE = os.path.join(os.path.dirname(__file__), "inventory.xlsx")

# Laden/Schreiben mit Pandas

def load_items():
    """Lädt die Tabelle aus der Excel-Datei und gibt sie als Liste von
    Dictionaries zurück. Falls die Datei nicht existiert, wird eine leere
    Liste geliefert (oder es kann eine Beispiel-Liste erzeugt werden)."""
    if not os.path.exists(EXCEL_FILE):
        # Datei existiert noch nicht – nichts zu laden
        return []

    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception:
        # z.B. ungültiges Format oder Lesefehler
        return []

    # Sicherstellen, dass die benötigten Spalten vorhanden sind
    cols = [c.lower() for c in df.columns]
    has_id = "id" in cols
    has_name = "name" in cols
    has_qty = "qty" in cols or "menge" in cols

    items = []
    for idx, row in df.iterrows():
        # ID bestimmen - falls nicht vorhanden, aus dem Index generieren
        _id = int(row["id"]) if has_id else idx + 1
        name = row["name"] if has_name else f"Item {_id}"
        qty = int(row["qty"]) if has_qty else int(row.get("menge", 0))
        items.append({"id": _id, "name": name, "qty": qty})
    return items


def save_items(items):
    """Schreibt die aktuelle Liste wieder in die Excel-Datei. Die Reihenfolge
    und die Stückzahlen werden dabei beibehalten."""
    df = pd.DataFrame(items)
    try:
        df.to_excel(EXCEL_FILE, index=False)
    except Exception as exc:
        # Bei Fehlern hier könnten wir loggen oder eine Exception weiterreichen
        print("Fehler beim Speichern der Excel-Datei:", exc)


# Globale Liste, initialisiert beim Start des Servers
ITEMS = load_items()

# Wenn es keine Werte in der Tabelle gibt, kann man optional ein paar Beispiel-
# Elemente anlegen. Die Zeilen unten können auskommentiert werden, wenn man das
# nicht möchte.
if not ITEMS:
    ITEMS = [
        {"id": 1, "name": "Nägel", "qty": 5},
        {"id": 2, "name": "Schrauben", "qty": 12},
        {"id": 3, "name": "Hammer", "qty": 1},
        {"id": 4, "name": "Dübel", "qty": 20},
        {"id": 5, "name": "Säge", "qty": 2},
        {"id": 6, "name": "Zange", "qty": 1},
    ]
    # Beim ersten Start auch gleich in Excel schreiben, damit die Datei existiert
    save_items(ITEMS)

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

    # Änderungen sofort in die Excel-Datei schreiben
    save_items(ITEMS)

    return jsonify({"ok": True, "count": len(ITEMS)})

@app.route("/data", methods=["GET"])
def data():
    # Optional: zum Debuggen
    return jsonify(ITEMS)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
