# Massive Aktien-Abfrage

Kleine Desktop-Anwendung mit grafischer Oberfläche (tkinter), die Aktienkurse über die
[Massive API](https://massive.com) (früher Polygon.io) abruft und als Diagramm darstellt.

## Funktionen

- **Letzter Handelstag:** Eröffnung, Hoch, Tief und Schluss einer Aktie anzeigen
- **Bestimmter Tag:** Dieselben Werte für ein frei wählbares Datum in der Vergangenheit
- **Diagramm bis heute:** Ab einem Startdatum wird für jeden Handelstag ein Punkt (Schlusskurs)
  gezeichnet, dazu ein Band von Tief bis Hoch des Tages

## Voraussetzungen

- Python 3.8 oder neuer
- Die Pakete `requests` und `matplotlib`
- tkinter (bei Windows und macOS in Python enthalten; unter Linux ggf. `sudo apt install python3-tk`)
- Ein kostenloser API-Key von Massive

## Installation

1. Abhängigkeiten installieren:

   ```bash
   pip install requests matplotlib
   ```

2. API-Key erstellen: Konto auf [massive.com](https://massive.com) anlegen und den Key unter
   [massive.com/dashboard/keys](https://massive.com/dashboard/keys) kopieren.

3. Den Key im Code eintragen (oben in der Datei):

   ```python
   api_key = "DEIN_API_KEY"
   ```

> **Wichtig:** Den Key nicht veröffentlichen (z. B. auf GitHub oder in Chats). Wenn er doch
> öffentlich geworden ist, im Massive-Dashboard einen neuen erzeugen.

## Starten

```bash
python aktien_abfrage.py
```

(Dateiname bei Bedarf an deine Datei anpassen.)

## Bedienung

| Feld / Button | Bedeutung |
| --- | --- |
| **Aktien-Ticker** | Kürzel der Aktie in Großbuchstaben, z. B. `AAPL`, `TSLA`, `MSFT` |
| **Startdatum** | Format `JJJJ-MM-TT`, z. B. `2026-10-15`. Leer lassen für den letzten Handelstag |
| **Abfragen** | Zeigt die Werte für den letzten Handelstag bzw. für das eingegebene Datum |
| **Diagramm bis heute** | Zeichnet alle Handelstage vom Startdatum bis heute (Startdatum ist Pflicht) |
| **Enter-Taste** | Löst „Abfragen" aus |

Die Statuszeile unter den Ergebnissen zeigt, ob die Abfrage geklappt hat oder ein Fehler
aufgetreten ist.

## So funktioniert es

Der Code ruft die REST-API von Massive mit `requests` ab und wandelt die Antwort in JSON um.

- `daten_holen(ticker, von, bis)` ruft den Endpunkt
  `/v2/aggs/ticker/{ticker}/range/1/day/{von}/{bis}` ab (Tageskerzen für einen Zeitraum).
- `abfragen()` zeigt die Werte eines einzelnen Tages. Ohne Datum wird der Endpunkt
  `/v2/aggs/ticker/{ticker}/prev` (letzter Handelstag) verwendet.
- `diagramm()` holt alle Tageskerzen vom Startdatum bis heute und zeichnet sie mit
  matplotlib in das Fenster.

In der API-Antwort stehen die Werte unter `results` mit diesen Kürzeln:

| Kürzel | Bedeutung |
| --- | --- |
| `o` | Eröffnung (open) |
| `h` | Tageshoch (high) |
| `l` | Tagestief (low) |
| `c` | Schlusskurs (close) |
| `v` | Handelsvolumen |
| `t` | Zeitstempel in Millisekunden |

## Einschränkungen

- **Kostenloser Plan:** Maximal 2 Jahre Historie und 5 Anfragen pro Minute. Ein zu altes
  Startdatum oder zu viele Anfragen führen zu einem Fehler.
- **Wochenenden und Feiertage:** Für diese Tage gibt es keine Daten. Bei einer Abfrage genau
  dieses Tages erscheint „something went wrong"; im Diagramm fehlen die Punkte einfach.
- **Aktueller Tag:** Tagesdaten gibt es erst nach Börsenschluss. Es sind immer Daten des
  Vortags oder älter.
- Die Zeitangaben der API beziehen sich auf die US-Ostküstenzeit (Eastern Time).

## Fehlersuche

Bei „something went wrong" in der Statuszeile kannst du dir in `abfragen()` mit den bereits
vorhandenen `print(...)`-Zeilen die Antwort der API im Terminal ansehen. Häufige Ursachen:

- Ungültiger oder fehlender API-Key (Antwort enthält einen Fehlerstatus statt `results`)
- Ticker in Kleinbuchstaben oder unbekanntes Kürzel
- Datum im falschen Format oder an einem Wochenende/Feiertag
- Zu viele Anfragen in kurzer Zeit (Limit von 5 pro Minute)
- Startdatum liegt außerhalb des Zeitraums, den dein Plan abdeckt

## Quellen

- [Massive API Dokumentation](https://massive.com/docs/rest/quickstart)
- [Custom Bars (OHLC)](https://massive.com/docs/rest/stocks/aggregates/custom-bars.md)
- [Previous Day Bar (OHLC)](https://massive.com/docs/rest/stocks/aggregates/previous-day-bar.md)
