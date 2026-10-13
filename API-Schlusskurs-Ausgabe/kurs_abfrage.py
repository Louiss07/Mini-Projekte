import os
import requests as rq
from dotenv import load_dotenv
import sys
import sqlite3
from pathlib import Path


BASIS = Path(__file__).resolve().parent
    



def hole_schlusskurs(symbol, api_key):
    
    api = "https://www.alphavantage.co/query"

    r = rq.get(
        api, 
        params={"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key},
        timeout=10

        )
    r.raise_for_status()
    daten = r.json()

    group = daten.get("Global Quote")

    if not group:
        raise ValueError(f"{symbol}: Keine Vorhandenen daten !")
    
    kurs = float(group["05. price"])
    datum = group["07. latest trading day"]

    return kurs, datum


def erstelle_tabelle(con):
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS schlusskurse (
                id INTEGER PRIMARY KEY,
                datum TEXT NOT NULL,
                symbol TEXT NOT NULL,
                kurs REAL NOT NULL,
                UNIQUE(symbol, datum)
    )

""")
    con.commit()

def speichere_kurs(con, symbol, datum, kurs):
    with con:
        cur = con.cursor()
        cur.execute("INSERT OR IGNORE INTO schlusskurse (datum, symbol, kurs) VALUES (?, ?, ?)",
            (datum, symbol, kurs))
    

    if cur.rowcount == 1:
        return True
    else:
        return False





def main(symbol):


    load_dotenv(BASIS / ".env")

    api_key = os.getenv("ALPHA_VANTAGE_KEY")

    if api_key is None:
        print("Keine .env mit API Key hinterlegt oder ALPHA_VANTAGE_KEY variable fehlt")
        sys.exit(1)

    if api_key == "":
        print("Kein API Key in der .env hinterlegt")
        sys.exit(1)


    try:
        kurs, datum = hole_schlusskurs(symbol, api_key)

    except rq.exceptions.Timeout as e:
        print(f"Fehler Timeout")
        sys.exit(1)

    except rq.exceptions.HTTPError as e:
        print(f"Fehler HTTP Error: {e.response.status_code}")#type: ignore
        sys.exit(1)

    except rq.exceptions.ConnectionError:
        print(f"Fehler bei Verbindung: Netzwerk oder DNS-Problem, API nicht erreichbar")
        sys.exit(1)

    except ValueError as e:
        print(f"Value Error: {e}")
        sys.exit(1)

    con = sqlite3.connect(BASIS / "kurse.db")
    erstelle_tabelle(con)
    neu = speichere_kurs(con, symbol, datum, kurs)
    if neu == True: 
        print(f"{symbol}: {datum} - {kurs:.2f}USD gespeichert")
    else:
        print("Schon vorhanden")
    con.close()




if __name__ == "__main__":
    main("SPY")


