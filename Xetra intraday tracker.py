import yfinance as yf
import pandas as pd
from datetime import datetime

# Aktien-Ticker (Yahoo Finance, Xetra)
TICKERS = {
    "Siemens_AG": "SIE.DE",
    "Allianz_SE": "ALV.DE",
    "Rheinmetall_AG": "RHM.DE",
    "Deutsche_Telekom_AG": "DTE.DE"
}

# Aktuelles Datum
today = datetime.now().strftime('%Y-%m-%d')

# Leere Liste für alle Tagesdaten
all_data = []

# CSV-Dateiname für die fortlaufende Datei
csv_filenames = ["SIE_intraday.csv", "ALV_intraday.csv", "RHM_intraday.csv", "DTE_intraday.csv"]

# Durchlaufe alle Ticker und hole die heutigen stündlichen Daten
laufvariable = 0
for name, ticker in TICKERS.items():
    stock = yf.Ticker(ticker)
    df = stock.history(interval="30m", period="1d")

    if df.empty:
        print(f"⚠️ Keine Daten für {name} ({ticker}) gefunden.")
        continue

    df.reset_index(inplace=True)
    df['Unternehmen'] = name
    df['Datum'] = df['Datetime'].dt.date
    df['Uhrzeit'] = df['Datetime'].dt.strftime('%H:%M:%S')
    df = df[['Datum', 'Uhrzeit', 'Unternehmen', 'Close']].rename(columns={'Close': 'Kurs_EUR'})
    # Prüfe, ob Datei existiert → falls ja: anhängen, sonst erstellen
    try:
        existing_df = pd.read_csv(csv_filenames[laufvariable])
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    # Duplikate vermeiden (Datum + Uhrzeit + Unternehmen eindeutig)
    updated_df.drop_duplicates(subset=['Datum', 'Uhrzeit', 'Unternehmen'], inplace=True)

    # Speichern
    updated_df.to_csv(csv_filenames[laufvariable], index=False, encoding='utf-8')
    print(f"✅ {len(df)} neue Einträge angehängt. Gesamt: {len(updated_df)} Zeilen.")

    laufvariable += 1

