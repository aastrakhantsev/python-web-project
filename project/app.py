import requests
import telebot
from bs4 import BeautifulSoup
from portfolio import wal

bot = telebot.TeleBot('5157785277:AAHiFt0hFK7YkABLgHLIU46xjuUjN-9lcgQ')


def get_rate(ticker):
    response = requests.get(f'https://finance.yahoo.com/quote/{ticker}-USD?p={ticker}-USD')
    html = BeautifulSoup(response.text, 'html.parser')
    x = str(html.select('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\).D\(ib\).smartphone_Mb\(10px\).W\(100\%\)--mobp > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)'))
    ans = ""
    for i in range(x.find('value="') + 7, len(x)):
        if x[i] == '\"':
            break
        ans += x[i]
    return ans


@bot.message_handler(commands=['start', 'help'])
def main(message):
    text = "/help - to see this message \n"
    text += "/guide - to know basics of interaction \n\n"
    text += "/rate - core function \n"
    text += "/add - add currency to your wallet\n"
    text += "/remove - remove currency to your wallet\n"
    text += "/wallet - get wallet info\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['guide'])
def guide(message):
    text = "<i>/rate</i>\n"
    text += "Enter  <b>/rate + [ticker]</b>    to get rate of cryptocurrency\n\n"
    text += "<i>/add</i>\n"
    text += "Enter  <b>/add + [ticker] + [number]</b>    to add <i>number</i> of needed currency to your wallet\n\n"
    text += "<i>/remove</i>\n"
    text += "Enter  <b>/remove + [ticker] + [number]</b>    to remove <i>number</i> of needed currency to your wallet\n\n"
    text += "<i>/wallet</i>\n"
    text += "Enter  <b>/wallet</b>    to get your portfolio"
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['rate'])
def rate(message):
    ticker = (message.text.split(' ')[1])
    val = get_rate(ticker)
    text = f"One <b>{ticker}</b> is <b>${val}</b>"
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['add'])
def add(message):
    ticker = (message.text.split(' ')[1])
    num = (message.text.split(' ')[2])
    if ticker in wal:
        wal[ticker] += num
    else:
        wal[ticker] = num
    bot.send_message(message.chat.id, f'{num} of {ticker} added to wallet', parse_mode='html')


@bot.message_handler(commands=['remove'])
def remove(message):
    ticker = (message.text.split(' ')[1])
    num = (message.text.split(' ')[2])
    if ticker in wal:
        wal[ticker] -= num
        if wal[ticker] < 0:
            wal.pop(ticker)
    else:
        bot.send_message(message.chat.id, f'No {ticker} in your wallet', parse_mode='html')
    bot.send_message(message.chat.id, f'{num} of {ticker} removed from wallet', parse_mode='html')


@bot.message_handler(commands=['wallet'])
def wallet(message):
    text = ""
    summary = 0
    for (key, value) in wal:
        text += f"{value} of {key},  which is <i>${value * get_rate(key)}</i>\n"
        summary += value * get_rate(key)
    text += f"\nYour wallet is {summary}"
    bot.send_message(message.chat.id, text, parse_mode='html')


bot.polling(none_stop=True)
