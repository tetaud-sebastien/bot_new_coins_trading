# bot_new_coins_trading

Create a virtual environment (Python 3.9) or use conda to create a virtual environment:

```
conda create --name <env_name> --clone base
OR
python -m venv <myenv>
```
In the virtual environment, upgrade pip and install dependencies using:

```
pip install --upgrade pip
pip install -r requirements.txt
```

File the config.json with exchange and email credentials: 

```json
{
    "exchange": {
        "binance": {
            "api_source_key": "api_source_key",
            "api_source_secret": "api_source_secret",
            "type": "spot"
        }
    },
    "email":{
        "email_adress":"email_adress",
        "email_password":"email_password"

    }
}
```

In order to run the bot, run the following cli in the project root directory:

```
cp config.json .config.json
```

Run the bot:

```
python main.py
```