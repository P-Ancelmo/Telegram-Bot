import random
import unicodedata
from time import sleep

from bs4 import BeautifulSoup
import requests

import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import datetime
import pytz

ids = []

def constituicao2(context: CallbackContext):

    url = 'https://www.meuvademecumonline.com.br/legislacao/constituicao_titulo/21/constituicao/'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    for s in soup.select('strike'):
        s.extract()

    artigos = [""]
    tudo = []
    i = 0
    c = True
    for linha in soup.get_text().split("\n"):
        linha = unicodedata.normalize("NFKD", linha)
        linha = linha.strip("\r")
        linha = linha.strip()
        if "Ulysses Guimarães" in linha:
            break
        if (not linha == "CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL." or linha == '') and c:
            #print("1" +linha)
            continue
        c = False
        if "Art." in linha:
            if not linha in artigos[i]:
                artigos.append(linha)
                i+=1
        if linha != '':
            tudo.append(linha)
    artigos.append(tudo[tudo.index(artigos[len(artigos)-1])])

    str1 = ""
    rand = random.randint(1,len(artigos)-2)
    nart = rand

    start = tudo.index(artigos[nart])
    end = tudo.index(artigos[nart+1])
    for j in range(start, end):
        if "TÍTULO " in tudo[j] or "CAPÍTULO " in tudo[j] or "Seção " in tudo[j] or "Ulysses Guimarães" in tudo[j]:
            break
        if(";" in tudo[j-1] or ":" in tudo[j-1] or ")" in tudo[j-1]) and ("I" in tudo[j] or "V" in tudo[j] or "X" in
                                                                          tudo[j] or "L" in tudo[j]):
            str1 += """
            """
        str1 += tudo[j]

    quant_carac = 4000
    mensagem = [str1[index:index+quant_carac] for index in range(0, len(str1), quant_carac)]
    print(ids)
    #for id in ids:
    for linha in mensagem:
        context.bot.send_message(-763089910, '*==CONSTITUIÇÃO==*',parse_mode = 'Markdown')
        context.bot.send_message(-763089910, linha)
        #await bot.sendMessage("975654789", linha)

updater = Updater(token='5207686085:AAFcBQjGb_3ZELorNWRFF6YQ23CeJJwn64E', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def codigo_de_etica():
    url = 'https://www.meuvademecumonline.com.br/legislacao/constituicao_titulo/21/constituicao/'
    # get page
    page = requests.get(url)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.get_text())
    artigos = [""]
    tudo = []
    i = 0
    c = True

    for linha in soup.get_text().split("\n"):
        linha = unicodedata.normalize("NFKD", linha)
        linha = linha.strip("\r")
        linha = linha.strip()

        # if "Ulysses Guimarães" in linha and pedido == "Constituição":
        #     break
        if linha == '':
             #print("1" +linha)
             continue
        c = False
        if "Art." in linha:
            if not linha in artigos[i]:
                artigos.append(linha)
                #print(linha)
                i += 1
        if linha != '':
            tudo.append(linha)
    str1 = ""
    rand = random.randint(1, len(artigos) - 2)
    nart = 1

    start = tudo.index(artigos[nart])
    end = tudo.index(artigos[nart + 1])
    for j in range(start, end):

        if "TÍTULO " in tudo[j] or "CAPÍTULO " in tudo[j] or "Seção " in tudo[j] or "Ulysses Guimarães" in tudo[j]:
            break
        if (";" in tudo[j - 1] or ":" in tudo[j - 1] or ")" in tudo[j - 1]) or "." in tudo[j-1] and (
                "I" in tudo[j] or "V" in tudo[j] or "X" in
                tudo[j] or "L" in tudo[j]):
            str1 += """
                """
        str1 += tudo[j]

    quant_carac = 4000
    mensagem = [str1[index:index + quant_carac] for index in range(0, len(str1), quant_carac)]

    # for id in ids:
    for linha in mensagem:
        print(linha)

    #artigos.append(tudo[tudo.index(artigos[len(artigos) - 1])])

def start(update, context):
    message = 'Bem vindoooo'
    ids.append(update.effective_chat.id)
    context.bot.send_message(chat_id=975654789, text=message)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    j = updater.job_queue
    #j.run_once(constituicao2, 10)
    #target_time = datetime.time(hour=14,minute=45,second=00).replace(tzinfo=pytz.timezone('America/Sao_Paulo'))
    #j.run_daily(constituicao2, days=(0,1,2,3,4,5,6),time=target_time)
    # j.run_repeating(constituicao2, 3600, 1, datetime.time(hour=22, minute=00, second=00))
    j.run_repeating(constituicao2, 60, 1)
    #print(ids)
    updater.start_polling()
    print('Listening ...')
    #codigo_de_etica()


if __name__ == '__main__':
    main()
