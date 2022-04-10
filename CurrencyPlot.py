import matplotlib
import pandas as pd
import mplfinance as mpf
from matplotlib.pyplot import savefig
from pycoingecko import CoinGeckoAPI
import datetime
import sqlite3
import json

reformatted_data = dict()

def paint_plot(id_of_cur, days):
    result = get_exact_value_json(id_of_cur)
    currency = CoinGeckoAPI().get_coin_ohlc_by_id(id=result, vs_currency='usd', days=days)
    reformatted_data['Date'] = []
    reformatted_data['Open'] = []
    reformatted_data['High'] = []
    reformatted_data['Low'] = []
    reformatted_data['Close'] = []
    for dict in currency:
        reformatted_data['Date'].append(datetime.datetime.fromtimestamp(dict[0]/1000))
        reformatted_data['Open'].append(dict[1])
        reformatted_data['High'].append(dict[2])
        reformatted_data['Low'].append(dict[3])
        reformatted_data['Close'].append(dict[4])
    pdata = pd.DataFrame.from_dict(reformatted_data)
    pdata.set_index('Date', inplace=True)
    result = mpf.plot(pdata, type='line', savefig='foo.png')

def get_exact_value_json(id_of_cur):
    sqlite_connection = sqlite3.connect('coins.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    cursor.execute("SELECT cm.id, lower(cm.name) FROM Coins_Markets cm WHERE lower(cm.name) = '{}' or cm.id = '{}'".format(id_of_cur, id_of_cur))
    dataDb = cursor.fetchone()
    cursor.close()
    print(dataDb)
    f = open('response_crypto.json', errors='ignore')
    data = json.load(f)
    f.close()
    for i in data:
        if i['id'] == dataDb[0]:
            result = i['id']
            print(i)
    return result
    
    