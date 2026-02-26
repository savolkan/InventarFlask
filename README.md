# Inventar App

Diese kleine Flask-Anwendung zeigt eine Inventarliste an
die aus einer Excel-Datei (`inventory.xlsx`) geladen wird. Du kannst die
Stückzahlen direkt im Browser ändern und durch drücken von "Fertig /
Speichern" werden die Änderungen zurück in die Excel-Datei geschrieben.

## Vorbereitung

1. Python 3.10+ installieren.
2. Abhängigkeiten installieren:
   ```powershell
   pip install -r requirements.txt
   ```
3. Optional: Erstelle eine `inventory.xlsx` mit den Spalten `id`, `name`, `qty`.
   Wenn die Datei fehlt, wird beim ersten Start eine Beispiel-Datei angelegt.

## Starten

```powershell
python app.py
```

Danach im Browser `http://127.0.0.1:5000/` öffnen.
