from vk.init_bot import vk
from vk_api.utils import get_random_id
import aiohttp
import requests

DATA_USER = {}


def send_message(user_id, text, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard() if keyboard else None,
    )


def start_command(user_id):
    send_message(user_id, "Это чат бот трекинга привычек")


def help_command(user_id):
    help_text = f"""
    start - Начать работу
    help - Показать эту справку
    get_habit - Показать все привычки
    add_habit - Добавить новую привычку
    del_habit - Удалить привычку
    update_habit - Изменить название привычки
    done_habit - Подтвердить выполнение 
    not_done_habit - Подтвердить не выполнение
"""
    send_message(user_id, help_text)


def get_habits_command(user_id):
    url = f"http://api:6000/get_habits/{user_id}"

    try:
        resp = requests.get(url)

        if resp.status_code != 200:
            send_message(user_id, "У вас нет привычек")
            return

        data = resp.json()

        habits = data["habit_data"]

        text = "*Ваши привычки:*\n\n"

        for habit in habits:

            habit_id = habit.get("habit_id", "—")
            habit_name = habit.get("habit_name", "Без названия")
            days = habit.get("days", 0)
            created_at = habit.get("created_at", "")

            if created_at:
                created_at = str(created_at)[:10]

            text += f" {habit_name}\n"
            text += f" ID: `{habit_id}`\n"
            text += f" Дней: {days}\n"
            text += f" Создано: {created_at}\n\n"

        send_message(user_id, text)

    except Exception as e:
        print(f"ERROR: {e}")
        send_message(user_id, f"Ошибка: {str(e)}")


def add_habit_start(user_id):
    DATA_USER[user_id] = {"action": "add_habit"}
    send_message(user_id, "Напиши название привычки")


def add_habit_process(user_id, habit_name):
    url = f"http://api:6000/create_habit/{user_id}/{habit_name}"
    resp = requests.post(url)
    if resp.status_code == 200:
        data = resp.json()
        habit_id = data.get("habit_id", "")
        send_message(user_id, f"Привычка создана ID - {habit_id}")
    else:
        send_message(user_id, f"Произошла ошибка - {resp.status_code}")

    if user_id in DATA_USER:
        del DATA_USER[user_id]


def delete_habit_start(user_id):
    send_message(user_id, "напишите ID привычки")
    DATA_USER[user_id] = {"action": "del_habit"}


def delete_habit_process(user_id, habit_id):
    url = f"http://api:6000/delete_habit/{habit_id}/{user_id}"
    resp = requests.delete(url)
    if resp.status_code == 200:
        send_message(user_id, "Привычка удалена")
    else:
        send_message(user_id, f"Произошла ошибка {resp.status_code}")

    if user_id in DATA_USER:
        del DATA_USER[user_id]


def update_habit_start(user_id):
    send_message(user_id, "Напишите ID привычки которую хотите изменить")
    DATA_USER[user_id] = {"action": "waiting_for_habit_id"}


def process_new_name(user_id, habit_id):
    send_message(user_id, "Напишите новое название привычки")
    DATA_USER[user_id] = {"action": "waiting_for_new_name", "habit_id": habit_id}


def update_habit_request(user_id, habit_name, habit_id):
    url = f"http://api:6000/update_habit/{user_id}/{habit_id}/{habit_name}"
    resp = requests.put(url)
    if resp.status_code == 200:
        send_message(user_id, "Привычка обновлена")
    else:
        send_message(user_id, f"Произошла ошибка {resp.status_code}")

    if DATA_USER[user_id]:
        del DATA_USER[user_id]

def done_habit_start(user_id):
    send_message(user_id, 'напиши ID привычки которую хочешь отметить выполненной')
    DATA_USER[user_id] = {"action": "done_habit"}

def done_habit_process(user_id, habit_id):
    url = f'http://api:6000/done_habit/{user_id}/{habit_id}'

    resp = requests.post(url)

    if resp.status_code != 200:
        send_message(user_id, f'Произошла ошибка {resp.status_code}')

    data = resp.json()
    message = data["message"]
    send_message(user_id, message)

    if DATA_USER[user_id]:
        del DATA_USER[user_id]

def not_done_habit_start(user_id):
    send_message(user_id, 'Напиши ID привычки которую не выполнил')
    DATA_USER[user_id] = {"action": "not_done_habit"}

def not_done_habit_process(user_id, habit_id):
    url = f'http://api:6000/not_done/{user_id}/{habit_id}'

    resp = requests.get(url)
    if resp.status_code != 200:
        send_message(user_id, f'Произошла ошибка {resp.status_code}')

    data = resp.json()
    message = data["message"]
    send_message(user_id, message)

    if DATA_USER[user_id]:
        del DATA_USER[user_id]