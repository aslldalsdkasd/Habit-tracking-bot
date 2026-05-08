from vk_api.longpoll import VkEventType
from vk.init_bot import long
from vk.handlers.command import *


def main():
    print("start")
    for event in long.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message_text = event.text

            if message_text == "start":
                start_command(user_id)

            elif message_text == "help":
                help_command(user_id)

            elif message_text == "get_habit":
                get_habits_command(user_id)

            elif message_text == "add_habit":
                add_habit_start(user_id)

            elif message_text == "del_habit":
                delete_habit_start(user_id)

            elif message_text == "update_habit":
                update_habit_start(user_id)

            elif message_text == 'done_habit':
                done_habit_start(user_id)

            elif message_text == 'not_done_habit':
                not_done_habit_start(user_id)

            elif user_id in DATA_USER:
                action = DATA_USER[user_id]["action"]
                if action == "waiting_for_habit_id":
                    process_new_name(user_id, event.text)

                elif action == "add_habit":
                    add_habit_process(user_id, event.text)

                elif action == "waiting_for_new_name":
                    habit_id = DATA_USER[user_id].get("habit_id")
                    update_habit_request(user_id, event.text, habit_id)

                elif action == "del_habit":
                    delete_habit_process(user_id, event.text)

                elif action == "update_habit":
                    DATA_USER[user_id]["habit_id"] = event.text
                    send_message(user_id, "✏️ Напиши новое название привычки")
                    DATA_USER[user_id]["action"] = "update_habit_name"

                elif action == "update_habit_name":
                    habit_id = DATA_USER[user_id].get("habit_id")
                    update_habit_request(user_id, habit_id, event.text)

                elif action == 'done_habit':
                    done_habit_process(user_id, event.text)

                elif action == 'not_done_habit':
                    not_done_habit_process(user_id, event.text)
            else:
                send_message(
                    user_id, 'Неизвестная команда. Напишите "help" для списка команд'
                )


if __name__ == "__main__":
    main()
