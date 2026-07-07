from datetime import datetime

import pandas as pd
import yfinance as yf

tickers = [
    "^FCHI",  # CAC 40 (Indice)
    "AI.PA",  # Air Liquide
    "AIR.PA",  # Airbus
    "ALO.PA",  # Alstom
    "MT.AS",  # ArcelorMittal
    "CS.PA",  # AXA
    "BNP.PA",  # BNP Paribas
    "EN.PA",  # Bouygues
    "CAP.PA",  # Capgemini
    "CA.PA",  # Carrefour
    "ACA.PA",  # Crédit Agricole
    "BN.PA",  # Danone
    "DSY.PA",  # Dassault Systèmes
    "ENGI.PA",  # Engie
    "EL.PA",  # EssilorLuxottica
    "RMS.PA",  # Hermès
    "KER.PA",  # Kering
    "OR.PA",  # L'Oréal
    "LR.PA",  # Legrand
    "MC.PA",  # LVMH
    "ML.PA",  # Michelin
    "ORA.PA",  # Orange
    "RI.PA",  # Pernod Ricard
    "PUB.PA",  # Publicis Groupe
    "RNO.PA",  # Renault
    "SAF.PA",  # Safran
    "SGO.PA",  # Saint-Gobain
    "SAN.PA",  # Sanofi
    "SU.PA",  # Schneider Electric
    "GLE.PA",  # Société Générale
    "STLAM.MI",  # Stellantis
    "STMPA.PA",  # STMicroelectronics
    "TEP.PA",  # Teleperformance
    "HO.PA",  # Thales
    "TTE.PA",  # TotalEnergies
    "URW.PA",  # Unibail-Rodamco-Westfield
    "VIE.PA",  # Veolia
    "DG.PA",  # Vinci
    "VIV.PA",  # Vivendi
    "WLN.PA",  # Worldline
]


def get_price():
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("regularMarketPrice") or info.get("currentPrice")

            if price is None:
                hist = stock.history(period="1d")
                price = hist["Close"].iloc[-1] if not hist.empty else None

            data[ticker] = {
                "Price": round(price, 2) if price else None,
                "Time": datetime.now().strftime("%H:%M:%S"),
            }

        except Exception as e:
            data[ticker] = {"Price": "Error", "Time": str(e)}

    df = pd.DataFrame(data).T
    print(f"Cours au {datetime.now().strftime("%H:%M:%S")}")
    print(df)
    return df


if __name__ == "__main__":
    get_price()
