from datetime import datetime

import pandas as pd
from libs.market_data.yahoo import get_price

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

if __name__ == "__main__":
    # STOCK VALUES
    data = {}
    for ticker in tickers:
        data[ticker] = get_price(ticker)

    df = pd.DataFrame(data).T
    print(f"Cours boursiers du CAC au {datetime.now().strftime('%H:%M')} :")

    print(df)
