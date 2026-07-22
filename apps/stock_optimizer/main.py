import logging
from datetime import datetime

import pandas as pd
from libs.market_data.yahoo import data_raw_csv, get_prices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tickers = {
    "^FCHI": "CAC 40 (Indice)",
    "AI.PA": "Air Liquide",
    "AIR.PA": "Airbus",
    "ALO.PA": "Alstom",
    "MT.AS": "ArcelorMittal",
    "CS.PA": "AXA",
    "BNP.PA": "BNP Paribas",
    "EN.PA": "Bouygues",
    "CAP.PA": "Capgemini",
    "CA.PA": "Carrefour",
    "ACA.PA": "Crédit Agricole",
    "BN.PA": "Danone",
    "DSY.PA": "Dassault Systèmes",
    "ENGI.PA": "Engie",
    "EL.PA": "EssilorLuxottica",
    "RMS.PA": "Hermès",
    "KER.PA": "Kering",
    "OR.PA": "L'Oréal",
    "LR.PA": "Legrand",
    "MC.PA": "LVMH",
    "ML.PA": "Michelin",
    "ORA.PA": "Orange",
    "RI.PA": "Pernod Ricard",
    "PUB.PA": "Publicis Groupe",
    "RNO.PA": "Renault",
    "SAF.PA": "Safran",
    "SGO.PA": "Saint-Gobain",
    "SAN.PA": "Sanofi",
    "SU.PA": "Schneider Electric",
    "GLE.PA": "Société Générale",
    "STLAM.MI": "Stellantis",
    "STMPA.PA": "STMicroelectronics",
    "TEP.PA": "Teleperformance",
    "HO.PA": "Thales",
    "TTE.PA": "TotalEnergies",
    "URW.PA": "Unibail-Rodamco-Westfield",
    "VIE.PA": "Veolia",
    "DG.PA": "Vinci",
    "VIV.PA": "Vivendi",
    "WLN.PA": "Worldline",
}

if __name__ == "__main__":
    logger.info("Récupération des prix pour %d tickers...", len(tickers))
    data = get_prices(tickers)

    for ticker, name in tickers.items():
        data[ticker]["Name"] = name

    df = pd.DataFrame(data).T
    df = df[["Name", "Price", "Time"]]
    df.index.name = "Ticker"

    print(f"CAC40 stock values at {datetime.now().strftime('%H:%M')} :")
    print(df)
    data_raw_csv(df)
