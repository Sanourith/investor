# COMMAND LIST

Clone the Git repository :
```bash
git clone https://github.com/Sanourith/investor.git
cd investor
```

Activate virtual environment and update pip with managed package & classic needs:
```bash
python3 -m venv venv_finance # create venv
source venv_finance/bin/activate # get into venv

pip install -r requirements.txt
pip install -e .

### FOR BITCOIN VALUES
python apps/btc_optimizer.py

### FOR STOCK VALUES
python apps/stock_optimizer/main.py
```
