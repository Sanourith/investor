#! /bin/bash

# cd ~/work/investor/postgres
# docker-compose up -d | true
cd ~/work/investor/

source venv_finance/bin/activate
python apps/btc_optimizer/main.py

sleep 1

python apps/stock_optimizer/main.py
deactivate

# cd ~/work/investor/postgres
# docker-compose down | true
