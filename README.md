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

# BOT ALERTING
Personalize your treshold_percentage into apps/btc_optimizer.py variable (default 8%)
It will allow alerting for +/- 8% on your cryptos

Then, you'll have to create a bot into your TELEGRAM ACCOUNT.
Here is how you do :
* start a new conversation with @BotFather
* call /mybots > If you don't have any, use /newbot instead
* cath your bot ID and put it into env/.env file
* start a new conversation with @your_bot_name (say hello, test for example)
* then, open a new internet tab and call API : https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates \
(replace <YOUR_TOKEN> with your complete token) and copy chat_id into env/.env file

TADAAAAAA
