import requests
import telebot
from bs4 import BeautifulSoup


bot = telebot.TeleBot('5157785277:AAHiFt0hFK7YkABLgHLIU46xjuUjN-9lcgQ')


@bot.message_handler(commands=['start', 'help'])
def main(message):
    text = "/help - to see this message \n/guide - to know basics of interaction \n\n"
    text += "/rate - core function \n/cancel"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['guide'])
def guide(message):
    text = "<b>1.</b> Press /rate - to get rate of cryptocurrency\n"
    text += "<b>2.</b> Enter cryptocurrency's ticker"
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['rate'])
def rate(message):
    ticker = (message.text.split(' ')[1])
    response = requests.get(f'https://finance.yahoo.com/quote/{ticker}-USD?p={ticker}-USD')
    html = BeautifulSoup(response.text, 'html.parser')
    x = html.select('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\).W\(100\%\).D\(ib\).smartphone_Mb\(10px\).W\(100\%\)--mobp > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > fin-streamer.Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)')
    x = str(x)
    ans = f"One <b>{ticker}</b> is <b>$</b>"
    for i in range(x.find('value="') + 7, len(x)):
        if x[i] == '\"':
            break
        ans += x[i]
    print(ans)
    bot.send_message(message.chat.id, ans, parse_mode='html')


bot.polling(none_stop=True)
