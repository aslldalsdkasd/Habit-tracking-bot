from telegram.main import bot
import aiohttp
import requests
DATA_USER = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Это чат бот для трекинга привычек")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, 'dsdsds')

@bot.message_handler(commands=['get_habit'])
def get(message):
    user_id = message.from_user.id
    url = f'http://api:6000/get_habit/{user_id}'
    resp = requests.get(url)
    if resp.status_code != 200:
        bot.send_message(message.chat.id, f'Ошибка: у вас нет привычек')
        return
    habits = resp.json()

    text = 'ваши привычки'

    for habit in habits:
        habit_id = habit.get('habit_id', '')
        habit_name = habit.get('habit_name', '')
        days = habit.get('days', 0)
        created_at = habit.get('created_at', '')

    text += f"{habit_name}\n ID - {habit_id}\n Дней пройдено - {days}\n Создано - {created_at}"


    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["add_habit"])
def create_habit(message):
     bot.send_message(message.chat.id, 'напиши название привычки')

     bot.register_next_step_handler(message, add_habit)

def add_habit(message):
    habit = message.text
    user_id = message.from_user.id

    url = f'http://api:6000/create_habit/{user_id}/{habit}'
    resp = requests.post(url)
    if resp.status_code == 201:
        data =  resp.json()
        habit_id = data.get('habit_id', '')
        bot.send_message(message.chat.id, f"привычка создана ID - {habit_id}")
    else:
        bot.send_message(message.chat.id, f'произошла ошибка {resp.status_code}')

@bot.message_handler(commands=["del_habit"])
def delete(message):
    bot.send_message(message.chat.id, 'напишите ID привычки которую хотите удалить')
    bot.register_next_step_handler(message, del_habit)

def del_habit(message):
    habit_id = message.text
    user_id = message.from_user.id
    url = f'http://api:6000/delete_habit/{habit_id}/{user_id}'
    resp = requests.delete(url)
    if resp.status_code == 204:
        bot.send_message(message.chat.id, 'привычка удалена')
    else:
        bot.send_message(message.chat.id, f'произошла ошибка {resp.status_code}')

@bot.message_handler(commands=["update_habit"])
def update(message):
    bot.send_message(message.chat.id, 'напиши ID привычки у которой хотите изменить название')
    bot.register_next_step_handler(message, update_habit)

def update_habit(message):
    habit_id = message.text
    user_id = message.from_user.id
    DATA_USER['habit_id'] = habit_id
    ms = bot.send_message(message.chat.id, 'Напиши новое название привычки')
    bot.register_next_step_handler(ms, process_new_name)

def process_new_name(message):
    habit_name = message.text
    user_id = message.from_user.id
    habit_id = DATA_USER.get('habit_id')
    update_habit_request(message, habit_name, habit_id)
    if "habit_id" in DATA_USER:
        del DATA_USER['habit_id']
def update_habit_request(message, habit_name, habit_id):

    url = f'http://api:6000/update_habit/{habit_id}/{habit_name}'

    resp = requests.put(url)
    if resp.status_code == 201:
        bot.send_message(message.chat.id, 'привычка обновлена')
    else:
        bot.send_message(message.chat.id, f'произошла ошибка {resp.status_code}' )

