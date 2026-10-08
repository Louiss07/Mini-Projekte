import requests as rq 
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt 



def hole_zeitreihe(start:date, ende:date, basis:str, ziel:str) -> dict[str, float]:
    api = "https://api.frankfurter.app"
    url = f"{api}/{start}..{ende}"

    r = rq.get(
        url,
        params={"base": basis, "symbols": ziel},
        timeout=10

    )
    daten = r.json()

    zeitreihe = {}
    for datum, preis in daten["rates"].items():
        kurs = preis[ziel]
        zeitreihe[datum] = kurs


    return zeitreihe
    


def main(basis:str, ziel:str, zeitraum:int):
    ende = date.today()
    start = ende - timedelta(days=zeitraum)
    kurse = hole_zeitreihe(start, ende, basis, ziel)


    s = pd.Series(kurse)
    s.index = pd.to_datetime(s.index)
    hoechste_d = s.idxmax()
    hoechste = s.max()
    niedrigste_d = s.idxmin()
    niedrigste = s.min()
    start_kurs = s.iloc[0]
    end_kurs = s.iloc[-1]
    veraenderung = (end_kurs - start_kurs) / start_kurs * 100

    line_style = dict(marker = ".",
                 markersize = 10, 
                markerfacecolor = "#FFFFFF",
                markeredgecolor = "#000000",
                 linestyle ="solid",
                linewidth =2
                )



    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(s.index, s.values, **line_style)  #type: ignore

    ax.set_title(f"Chart von {basis} zu {ziel}",fontsize= 20, fontweight="bold")
    ax.set_xlabel("Datum", fontsize= 15,fontweight="bold")
    ax.set_ylabel("Kurs", fontsize= 15, fontweight="bold")

    ax.grid(True, alpha=0.3)
    ax.scatter(hoechste_d, hoechste, zorder=2, s=15, color="green")#type: ignore
    ax.scatter(niedrigste_d, niedrigste, zorder=2, s=15, color="red")#type: ignore
    fig.autofmt_xdate() 
    fig.tight_layout()   



    fig.savefig(f"{basis}-{ziel}.png", dpi=300,)
    plt.show()
    plt.close(fig)

    print(f"Höchste: Am {hoechste_d.date()} bei {hoechste:.4f} €") #type: ignore
    print(f"Tiefste: Am {niedrigste_d.date()} bei {niedrigste:.4f} €") #type: ignore
    print(f"Start kurs lag bei {start_kurs:.4f} €")
    print(f"End kurs lag bei {end_kurs:.4f} €")
    print(f"Der Kurs hat sich um {veraenderung:+.2f}% verändert " )





if __name__ == "__main__":
    main("EUR", "JPY", 90)


