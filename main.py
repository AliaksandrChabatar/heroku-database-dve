import os # для работы с системными переменными
import telebot # для работы с Телеграммом
import logging # для логирования отладочной информации
from config import *
from flask import Flask, request # из библиотеки flask импортируем модуль flask (для настройки вертекса) и requests (для обработки запросов)
# из файла config.py импортируем
bot = telebot.TeleBot(BOT_TOKEN) # создаём переменную бот, в качестве аргумента в конструктор передаём токен нашего телебота
server = Flask(__name__) # создаём переменную server - это екземпляр класс Flask, в конструктор передаём имя текущего модуля
logger = telebot.logger # создаём переменную logger и
logger.setLevel(logging.DEBUG) # устанавливаем уровень логирования на ДЕБАГ (для отладочных сообщений с Heroku...)

# описываем логику взаимодействия при вводе пользователем команды старт: /start
@bot.message_handler(commands=["start"]) # декоратор указывающий что именно следующая функция отвечает за команду start
def start(message): # создаём саму функцию старта, для этого
    username = message.from_user.username # получив эту команду функция передаёт обьект-message. Из этого обьекта
    bot.reply_to(message, f"Hello, {username}!") # достанем имя пользователя и поприветствуем его (методом reply_to).

# реализовываем направление входящих сообщений с сервера (Github) нашему телеграм-боту
@server.route(f"/{BOT_TOKEN}", methods=["PORT"]) # через декоратор и
def redirect_message(): # функцию redirect_message
    json_string = request.get_data().decode("utf-8") # получаем данные от сервера в utf-8 формате
    update = telebot.types.Update.de_json(json_string) # и применим их к боту
    bot.process_new_updates([update]) # с помощью вызова метода process_new_updates
    return "!", 200

if __name__ == "__main__": # конструкция гарантирующая, что сервер запустится только при непосредственном...main скрипта)
    bot.remove_webhook() # устанваливаем и обнавляем webhook для нашего бота (удаляем текущий и устанавливаем новый)
    bot.set_webhook(url=APP_URL) # устанваливаем url нашего приложения
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) # запускаем сервер с помощью метода run,
    # передав в него аргументы: host с нулями (это позволит сделать сервер публичным, а не локальным)
    # и port: воспользуемся модулем os и возьмём переменную PORT и значение

