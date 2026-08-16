#! /bin/bash

set -e

cd ~/work/investor

source venv_finance/bin/activate
python apps/btc_optimizer/main.py

sleep 1

python apps/stock_optimizer/main.py
deactivate
