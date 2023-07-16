import telebot
import httplib2
import apiclient.discovery
from oauth2cliet.service_account import ServiceAccountCredentials
from telebot import types
import datetime

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


bot = telebot.TeleBot("Токен бота для БургерКит")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Выполнено")
    button2 = types.KeyboardButton("Не сделано")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, text ="Привет,я бот для компании БургерКит?,отслеживаю выполнение задач.".format(message.from_user),reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == 'Выполнено'):
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOprion":"USER_ENTERED",
            "data": [
                {
                    "range":"Лист номер один!D1:E1",
                    'majorDimension':"ROWS",
                    "values": [
                        ['время','время на ответ'],
                        [datetime.datetime.now(),]
                    ]
                }
            ]
        }
        bot.send_message('Тут должен быть ID чата или пользователя куда отправить сообщение',f'{message.from_user.username}.Выполнено')
    if(message.text =='Не сделаено'):
        bot.send_message('Тут должен быть ID чата или пользователя куда отправить сообщение',f'{message.from_user.username}.Не сделано')
bot.infinity_polling()