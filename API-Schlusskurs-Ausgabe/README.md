# API-Schlusskurs-Ausgabe

Python-Skript, das den aktuellen Schlusskurs eines Wertpapiers über die Alpha-Vantage-API abruft und in einer lokalen SQLite-Datenbank speichert. Gebaut, um später automatisch jeden Abend zu laufen.

## Was es macht

- Holt Kurs und Handelstag für ein Symbol (Standard: `SPY`, ETF auf den S&P 500)
- Speichert den Kurs in `kurse.db`, die Tabelle wird beim ersten Lauf automatisch angelegt
- Verhindert doppelte Einträge: Pro Symbol und Handelstag gibt es genau einen Datensatz
- Nimmt das Datum aus den API-Daten, nicht von der Systemuhr, damit am Wochenende und an Feiertagen keine falschen Einträge entstehen
- Findet `.env` und Datenbank immer relativ zum Skript, egal aus welchem Ordner es gestartet wird

## Robustheit

Jeder Fehlerfall wird abgefangen, mit einer klaren Meldung ausgegeben und mit Exit-Code `1` beendet:

| Fall | Ursache |
|------|---------|
| Fehlender API-Key | `.env` fehlt oder Variable nicht gesetzt |
| Timeout | API antwortet nicht innerhalb von 10 Sekunden |
| HTTP-Fehler | API antwortet mit 4xx/5xx |
| Verbindungsfehler | Kein Netzwerk oder DNS-Problem |
| Keine Daten | Ungültiges Symbol oder API-Limit erreicht |

Bei Erfolg endet das Skript mit Exit-Code `0`, auch wenn der Kurs schon gespeichert war. Fehlermeldungen geben den API-Key nie aus.

## Datenbank

Tabelle `schlusskurse`:

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| `id` | INTEGER | Primärschlüssel, automatisch |
| `datum` | TEXT | Handelstag laut API |
| `symbol` | TEXT | z.B. `SPY` |
| `kurs` | REAL | Kurs in USD |

`UNIQUE(symbol, datum)` verhindert Duplikate.

## Installation

Voraussetzung: Python 3.10 oder neuer und ein kostenloser API-Key von [Alpha Vantage](https://www.alphavantage.co/support/#api-key) (25 Anfragen pro Tag).

```bash
git clone <repo-url>
cd API-Schlusskurs-Ausgabe
python -m venv venv
```

venv aktivieren:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

API-Key hinterlegen: `.env.example` zu `.env` kopieren und den eigenen Key eintragen:

```
ALPHA_VANTAGE_KEY=dein_key
```

Die `.env` steht in der `.gitignore` und wird nie committet.

## Benutzung

```bash
python kurs_abfrage.py
```

Das Symbol wird im Aufruf am Ende von `kurs_abfrage.py` festgelegt:

```python
main("SPY")
```

Damit der gespeicherte Wert wirklich der Schlusskurs ist, sollte das Skript nach US-Börsenschluss laufen (nach 22 Uhr deutscher Zeit).

## Technik

- `requests` für den API-Abruf
- `python-dotenv` für den API-Key
- `sqlite3` und `pathlib` aus der Standardbibliothek

## Hintergrund

Entstanden als Übungsprojekt zur Verbindung von APIs, Python und SQLite.