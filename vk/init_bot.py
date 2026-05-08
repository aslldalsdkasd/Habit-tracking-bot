import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv()
import os

GROUP_ID = int(os.getenv("GROUP_ID"))
vk_session = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))
vk = vk_session.get_api()
long = VkLongPoll(vk_session, group_id=GROUP_ID)
