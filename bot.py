import urllib3
from bs4 import BeautifulSoup
import datetime
import pytz

from typing import Final
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final  = 'your-token-here'
BOT_USERNAME: Final = '@yourBot'
CHAT_ID: Final = 'chat-id'
url = 'https://ru.ufes.br/cardapio'

def getCardapioAlmoco():
    # Realiza a solicitação HTTP para obter o conteúdo da página
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response.status == 200:
        soup = BeautifulSoup(response.data, 'html.parser')

        # Encontre todos os elementos com a classe "views-field-body"
        body_elements = soup.find_all('div', class_='views-field-body')
        meal_index = 0

        if meal_index < len(body_elements):
            body_element = body_elements[meal_index]

            cardapio_data = []  # Lista para armazenar os cardápios

            data = {}
            current_key = None

            # Percorre os elementos dentro do div apropriado
            for element in body_element.find_all(['strong', 'p']):
                if element.name == 'strong':
                    # A tag <strong> indica uma nova chave
                    current_key = element.get_text(strip=True)
                    if current_key != "*Cardápio sujeito a alterações":
                        if current_key not in data:
                            data[current_key] = []  # Cria uma nova chave no dicionário
                elif element.name == 'p' and current_key:
                    # A tag <p> indica o valor associado à chave
                    value = element.get_text().strip()
                    data[current_key].append(value)

            # Remove o último elemento de cada chave no dicionário
            for tag in ["Salada", "Prato Principal", "Opção", "Acompanhamento", "Guarnição", "Sobremesa"]:
                if tag in data and data[tag]:
                    data[tag].pop()

            cardapio_data.append(data)

            if (meal_index == 0):
                formatted_data = "<b>Almoço:</b>\n"
            else:
                formatted_data = "<b>Janta:</b>\n"

            for title, items in data.items():
                formatted_data += f"<b>{title}:</b>\n"
                for item in items:
                    formatted_data += f"- {item}\n"

            # Converte a lista de cardápios em JSON
            #json_data = json.dumps(cardapio_data, ensure_ascii=False, indent=4)
            return formatted_data
        else:
            return 'Não foi possível obter o cardápio de hoje.'

    return None  # Retorna None se a solicitação falhar

def getCardapioJantar():
    # Realiza a solicitação HTTP para obter o conteúdo da página
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response.status == 200:
        soup = BeautifulSoup(response.data, 'html.parser')

        # Encontre todos os elementos com a classe "views-field-body"
        body_elements = soup.find_all('div', class_='views-field-body')
        meal_index = 1

        if meal_index < len(body_elements):
            body_element = body_elements[meal_index]

            cardapio_data = []  # Lista para armazenar os cardápios

            data = {}
            current_key = None

            # Percorre os elementos dentro do div apropriado
            for element in body_element.find_all(['strong', 'p']):
                if element.name == 'strong':
                    # A tag <strong> indica uma nova chave
                    current_key = element.get_text(strip=True)
                    if current_key != "*Cardápio sujeito a alterações":
                        if current_key not in data:
                            data[current_key] = []  # Cria uma nova chave no dicionário
                elif element.name == 'p' and current_key:
                    # A tag <p> indica o valor associado à chave
                    value = element.get_text().strip()
                    data[current_key].append(value)

            # Remove o último elemento de cada chave no dicionário
            for tag in ["Salada", "Prato Principal", "Opção", "Acompanhamento", "Guarnição", "Sobremesa"]:
                if tag in data and data[tag]:
                    data[tag].pop()

            cardapio_data.append(data)

            if (meal_index == 0):
                formatted_data = "<b>Almoço:</b>\n"
            else:
                formatted_data = "<b>Janta:</b>\n"

            for title, items in data.items():
                formatted_data += f"<b>{title}:</b>\n"
                for item in items:
                    formatted_data += f"- {item}\n"

            # Converte a lista de cardápios em JSON
            #json_data = json.dumps(cardapio_data, ensure_ascii=False, indent=4)
            return formatted_data
        else:
            return 'Não foi possível obter o cardápio de hoje.'

    return None  # Retorna None se a solicitação falhar


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a bot!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom!')

async def sendAlmoco(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text=getCardapioAlmoco(),parse_mode=constants.ParseMode.HTML)

async def sendJanta(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text=getCardapioJantar(),parse_mode=constants.ParseMode.HTML)


def handle_response(text: str) -> str:
    processed: str = text.lower();
    if 'hello' in processed:
        return 'Hello!'
    return 'I do not understand'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.add_error_handler(error)

    j = app.job_queue

    # Mensagem diaria do almoco
    dtAlmoco = datetime.time(hour=9,minute=0,tzinfo=pytz.timezone('Brazil/East'))
    j.run_daily(sendAlmoco,dtAlmoco,days=(1,2,3,4,5))

    # Mensagem diaria do jantar
    dtJantar = datetime.time(hour=15,minute=0,tzinfo=pytz.timezone('Brazil/East'))
    j.run_daily(sendJanta,dtJantar,days=(1,2,3,4,5))


    print('Polling...')
    app.run_polling(poll_interval=3)
