from flask import Flask, render_template, request, flash, redirect, jsonify
import datetime
import config, csv
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
app.secret_key = ''

client = Client(config.API_KEY, config.API_SECRET)

@app.route('/api', methods=['GET'])
def api():

    account = client.get_account()
    some_balance = []
    some_balance_symbol = []
    some_balance_amount = []

    exchange_info = client.get_exchange_info()
    # print(exchange_info)
    symbols = exchange_info['symbols']

    balances = account['balances']
    # Shows only things I have balance in 
    for balance in balances:
        if '0.000000' not in balance['free']:
            # print(balance['asset'])
            some_balance.append(balance)
            some_balance_symbol.append(balance['asset'])
            some_balance_amount.append(balance['free'])

    new_dict = dict(zip(some_balance_symbol, some_balance_amount))
    # print("somebalance: ", some_balance[0])
    # print("AAAND THE SYMBOL IS: ", some_balance_symbol)
    
    return new_dict

@app.route('/history')
def history():

    # Changin' date to proper format so that I can use it as a variable
    today = datetime.date.today()
    print(str(today).split("-"))
    splitted_day = str(today).split("-")

    dates = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10" : "Oct",
        "11" : "Nov",
        "12" : "Dec"
    }

    date = "{day} {month}, {year}".format(day=splitted_day[2], month=dates[splitted_day[1]], year=splitted_day[0])

    ####################################################################################################################

    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Aug, 2020", date)
    
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            'low': data[3], 
            'close': data[4]
            }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        symbol=request.form['symbol']
        quantity= request.form['quantity']
        print("You want to buy: ", symbol,"This much ", quantity)
        # order = client.create_order(symbol=request.form['symbol'], side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=request.form['quantity'])
    
    except Exception as e:
        flash(e,"error")

    return redirect('/') 