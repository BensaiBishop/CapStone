from yahoo_fin import stock_info
from tkinter import *
from main import get_account, getHistory, api
import warnings
import numpy as np
import pandas_datareader.data as web
import pandas as pd
from model import stock_model
from sklearn.preprocessing import MinMaxScaler


warnings.filterwarnings("ignore")

ACCOUNT = get_account()
PORTFOLIO_VALUE = ACCOUNT['equity']
HISTORY = getHistory()
DAY_PROFIT = np.round(HISTORY['profit_loss_pct'][-1], 5)
TOTAL_PROFIT = np.round(sum(HISTORY['profit_loss_pct']), 5)


# funcs
def stock_price():
    price = stock_info.get_live_price(e1.get())
    Current_stock.set(price)
    preds = get_data()
    str_stock.set(preds)


def portfolio():
    return PORTFOLIO_VALUE


def insertitem(item):
    listbox.insert(0, item)


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


def preprocess_data(df):
    scaler = MinMaxScaler()
    df = df.values.reshape(-1, 1)
    df = scaler.fit_transform(df)
    inputs = []
    for i in range(60, len(df)):
        inputs.append(df[i - 60:i, 0])
    inputs = np.array(inputs)
    inputs = np.reshape(inputs, (inputs.shape[0], inputs.shape[1], 1))
    return inputs, scaler


def get_data():
    end_date = pd.to_datetime('today')
    start_date = '2020-10-01'
    df = web.DataReader(e1.get(), 'yahoo', start_date, end_date)
    df = df['Close']
    prices, scaler = preprocess_data(df)
    preds = stock_model.predict(prices)
    inverse_preds = scaler.inverse_transform(preds)
    preds_last = inverse_preds[-1]
    return preds_last


master = Tk()
master.geometry("600x400")
Current_stock = StringVar()
str_stock = StringVar()

Label(master, text="Company Symbol : ").grid(row=0, sticky=W)
Label(master, text="Stock Result:").grid(row=3, sticky=W)
Label(master, text='Stock Predicted: ').grid(row=4, sticky=W)
Label(master, text="", textvariable=str_stock,
      ).grid(row=4, column=1, sticky=W)

result2 = Label(master, text="", textvariable=Current_stock,
                ).grid(row=3, column=1, sticky=W)

e1 = Entry(master)
e1.grid(row=0, column=1, sticky=W)

b = Button(master, text="Show", command=stock_price)
b.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5, sticky=W)

# portfolio value
Label(master, text='Total Profit : ' + str(TOTAL_PROFIT) + '%').grid(row=5, sticky=W)
Label(master, text='Day Profit : ' + str(DAY_PROFIT) + '%').grid(row=6, column=0, sticky=W)
Label(master, text='PORTFOLIO VALUE : $' + str(PORTFOLIO_VALUE)).grid(row=7, column=0, sticky=W)
Label(master).grid(row=10, sticky=W)
Label(master, text='CREATE ORDER :                                    ').grid(row=11, column=0, sticky=W)

stepTwo = LabelFrame(master, text="ORDERS: ")
stepTwo.grid(rowspan=10, columnspan=10, sticky='nsew',
             padx=5, pady=5, ipadx=5, ipady=5)

listbox = Listbox(stepTwo)
listbox.pack(fill='both', expand=True)


# create order
def place_order():
    api.submit_order(o1.get(), o2.get(), 'buy', 'market', 'day')


def submit_data():
    content = o1.get()
    price_stock = stock_info.get_live_price(o1.get())
    rounded = np.round(price_stock, 3)
    insertitem(content + ': ' + str(rounded))


o1 = Entry(master)
o1.grid(row=11, column=1)
o2 = Entry(master)
o2.grid(row=11, column=2)

b1 = Button(master, text='ORDER', command=combine_funcs(place_order, submit_data))
b1.grid(row=11, column=3, columnspan=2, rowspan=2, padx=5, pady=5, sticky=W)

mainloop()