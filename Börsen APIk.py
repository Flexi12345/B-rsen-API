import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime, date
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# pip install requests matplotlib

url = "https://api.massive.com/v2/aggs/ticker/"
api_key = "J5g2Uq8wgm6jXXvYljn8rY0CoLt5qm19"  # kostenlos auf massive.com/dashboard/keys


def daten_holen(ticker, von, bis):
    add_url = ticker + "/range/1/day/" + von + "/" + bis + "?apiKey=" + api_key
    return requests.get(url + add_url).json()  # umwandeln in json


def abfragen():
    ticker = eingabe.get()
    datum = eingabe_datum.get()
    if not ticker:
        status.config(text="Bitte einen Ticker eingeben.", foreground="red")
        return

    try:
        if datum:
            data = daten_holen(ticker, datum, datum)  # bestimmter Tag: von = bis
        else:
            data = requests.get(url + ticker + "/prev?apiKey=" + api_key).json()

        bar = data["results"][0]
        print(bar)
        print(data)
        felder["Aktie"].config(text=data["ticker"])
        felder["Eröffnung"].config(text=bar["o"])
        felder["Hoch"].config(text=bar["h"])
        felder["Tief"].config(text=bar["l"])
        felder["Schluss"].config(text=bar["c"])

        status.config(text="Daten geladen.", foreground="green")

    except:
        status.config(text="something went wrong", foreground="red")


def diagramm():
    ticker = eingabe.get()
    datum = eingabe_datum.get()
    if not ticker or not datum:
        status.config(text="Bitte Ticker und Startdatum eingeben.", foreground="red")
        return

    try:
        heute = date.today().strftime("%Y-%m-%d")
        data = daten_holen(ticker, datum, heute)  # Startdatum bis heute

        tage = []
        schluss = []
        hoch = []
        tief = []
        for bar in data["results"]:
            tage.append(datetime.fromtimestamp(bar["t"] / 1000).date())  # ms -> Datum
            schluss.append(bar["c"])
            hoch.append(bar["h"])
            tief.append(bar["l"])

        ax.clear()
        ax.fill_between(tage, tief, hoch, alpha=0.2, label="Tief - Hoch")
        ax.plot(tage, schluss, marker="o", markersize=4, label="Schluss")
        ax.set_title(data["ticker"] + " ab " + datum)
        ax.set_ylabel("Preis")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))
        ax.grid(True, alpha=0.3)
        ax.legend()
        figur.autofmt_xdate()
        canvas.draw()

        status.config(text=str(len(tage)) + " Tage geladen.", foreground="green")

    except:
        status.config(text="something went wrong", foreground="red")


# --- Fenster ---
fenster = tk.Tk()
fenster.title("Massive Aktien-Abfrage")
fenster.geometry("640x760")
fenster.resizable(False, False)
fenster.bind("<Return>", lambda event: abfragen())  # Enter-Taste funktioniert überall

rahmen = ttk.Frame(fenster, padding=15)
rahmen.pack(fill="both", expand=True)

ttk.Label(rahmen, text="Aktien-Ticker (z.B. AAPL, TSLA, MSFT) GROßBUCHSTABEN:").pack(anchor="w")

eingabe = ttk.Entry(rahmen, font=("Arial", 12))
eingabe.pack(fill="x", pady=(5, 10))
eingabe.focus()

ttk.Label(rahmen, text="Startdatum (JJJJ-MM-TT (max 2 Jahre), leer = letzter Handelstag):").pack(anchor="w")

eingabe_datum = ttk.Entry(rahmen, font=("Arial", 12))
eingabe_datum.pack(fill="x", pady=(5, 10))

knoepfe = ttk.Frame(rahmen)
knoepfe.pack(fill="x")
ttk.Button(knoepfe, text="Abfragen", command=abfragen).pack(side="left", fill="x", expand=True)
ttk.Button(knoepfe, text="Diagramm bis heute", command=diagramm).pack(side="left", fill="x", expand=True, padx=(8, 0))

# --- Ergebnisanzeige ---
tabelle = ttk.Frame(rahmen)
tabelle.pack(fill="x", pady=15)

felder = {}
for zeile, name in enumerate(["Aktie", "Eröffnung", "Hoch", "Tief", "Schluss"]):
    ttk.Label(tabelle, text=name + ":", font=("Arial", 10, "bold")).grid(
        row=zeile, column=0, sticky="w", pady=2
    )
    felder[name] = ttk.Label(tabelle, text="-", font=("Arial", 10))
    felder[name].grid(row=zeile, column=1, sticky="e", padx=(20, 0))
tabelle.columnconfigure(1, weight=1)

status = ttk.Label(rahmen, text="")
status.pack(anchor="w")

# --- Diagramm-Fläche ---
figur = Figure(figsize=(6, 3.2), dpi=100)
ax = figur.add_subplot(111)
canvas = FigureCanvasTkAgg(figur, master=rahmen)
canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))

fenster.mainloop()