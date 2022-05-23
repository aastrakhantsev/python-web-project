from bs4 import BeautifulSoup
from portfolio import wal
import aiohttp
import aiogram
import os

bot = aiogram.Bot(os.getenv('BOT_TOKEN'))
dispatcher = aiogram.dispatcher.Dispatcher(bot)
parse_mode = aiogram.types.ParseMode.HTML


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text(encoding='utf-8')


async def get_rate(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}-USD?p={ticker}-USD'
    text = await get(url)
    soup = BeautifulSoup(text, 'html.parser')
    result = str(soup.find('fin-streamer', attrs={'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).contents[0])
    return result


@dispatcher.message_handler(commands=['start', 'help'])
async def main(message):
    text = (
        '<i>/help</i> - to see this message \n'
        '<i>/guide</i> - to know basics of interaction \n\n'
        '<i>/rate</i> - core function \n'
        '<i>/add</i> - add currency to your wallet\n'
        '<i>/remove</i> - remove currency to your wallet\n'
        '<i>/wallet</i> - get wallet info\n'
    )
    await bot.send_message(message.chat.id, text, parse_mode=parse_mode)


@dispatcher.message_handler(commands=['guide'])
async def guide(message):
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
    await bot.send_message(message.chat.id, text, parse_mode=parse_mode)


@dispatcher.message_handler(commands=['rate'])
async def rate(message):
    ticker = (message.text.split(' ')[1])
    val = await get_rate(ticker)
    text = f'One <b>{ticker}</b> is <b>${val}</b>'
    await bot.send_message(message.chat.id, text, parse_mode=parse_mode)


@dispatcher.message_handler(commands=['add'])
async def add(message):
    ticker = (message.text.split(' ')[1])
    num = (message.text.split(' ')[2])
    if ticker in wal:
        wal[ticker] += float(num)
    else:
        wal[ticker] = float(num)
    await bot.send_message(message.chat.id, f'{num} {ticker} added to wallet', parse_mode=aiogram.types.ParseMode.HTML)


@dispatcher.message_handler(commands=['remove'])
async def remove(message):
    ticker = (message.text.split(' ')[1])
    val = (message.text.split(' ')[2])
    if val == 'all':
        val = wal[ticker]
    if ticker in wal:
        wal[ticker] -= float(val)
        if wal[ticker] <= 0:
            wal.pop(ticker)
    else:
        await bot.send_message(message.chat.id, f'No {ticker} in your wallet', parse_mode=parse_mode)
    await bot.send_message(message.chat.id, f'{val} {ticker} removed from your wallet', parse_mode=parse_mode)


@dispatcher.message_handler(commands=['wallet'])
async def wallet(message):
    text = ''
    summary = 0
    for key, value in wal.items():
        text += f'{float(value)} of {key},  that is <i>${float(value) * float(get_rate(key))}</i>\n'
        summary += float(value) * float(get_rate(key))
    text += f'\nYour wallet is <i>${summary}</i>'
    await bot.send_message(message.chat.id, text, parse_mode=parse_mode)


if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher)
