import os
import requests
import telebot
from bs4 import BeautifulSoup
from portfolio import wal

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


def get_rate(ticker):
    html = requests.get(f'https://finance.yahoo.com/quote/{ticker}-USD?p={ticker}-USD')
    soup = BeautifulSoup(html.text, 'html.parser')
    result = str(soup.find('fin-streamer', attrs={'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).contents[0])
    return result


@bot.message_handler(commands=['start', 'help'])
def main(message):
    text = (
        '/help - to see this message \n'
        '/guide - to know basics of interaction \n\n'
        '/rate - core function \n'
        '/add - add currency to your wallet\n'
        '/remove - remove currency to your wallet\n'
        '/wallet - get wallet info\n'
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['guide'])
def guide(message):
    text = (
        '<i>/rate</i>\n'
        'Enter  <b>/rate + [ticker]</b>    to get rate of cryptocurrency\n\n'
        '<i>/add</i>\n'
        'Enter  <b>/add + [ticker] + [number]</b>    to add <i>number</i> of needed currency to your wallet\n\n'
        '<i>/remove</i>\n'
        'Enter  <b>/remove + [ticker] + [number]</b>    to remove <i>number</i> of needed currency to your wallet\n\n'
        '<i>/wallet</i>\n'
        'Enter  <b>/wallet</b>    to get your portfolio'
    )
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['rate'])
def rate(message):
    ticker = (message.text.split(' ')[1])
    val = get_rate(ticker)
    text = f'One <b>{ticker}</b> is <b>${val}</b>'
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['add'])
def add(message):
    ticker = (message.text.split(' ')[1])
    num = (message.text.split(' ')[2])
    if ticker in wal:
        wal[ticker] += float(num)
    else:
        wal[ticker] = float(num)
    bot.send_message(message.chat.id, f'{num} {ticker} added to wallet', parse_mode='html')


@bot.message_handler(commands=['remove'])
def remove(message):
    ticker = (message.text.split(' ')[1])
    num = (message.text.split(' ')[2])
    if num == 'all':
        num = wal[ticker]
    if ticker in wal:
        wal[ticker] -= float(num)
        if wal[ticker] <= 0:
            wal.pop(ticker)
    else:
        bot.send_message(message.chat.id, f'No {ticker} in your wallet', parse_mode='html')
    bot.send_message(message.chat.id, f'{num} {ticker} removed from wallet', parse_mode='html')


@bot.message_handler(commands=['wallet'])
def wallet(message):
    text = ''
    summary = 0
    for item in wal.items():
        key = item[0]
        value = item[1]
        text += f'{float(value)} of {key},  that is <i>${float(value) * float(get_rate(key))}</i>\n'
        summary += float(value) * float(get_rate(key))
    text += f'\nYour wallet is <i>${summary}</i>'
    bot.send_message(message.chat.id, text, parse_mode='html')


bot.polling(none_stop=True)
