import telebot
from dotenv import load_dotenv
load_dotenv()
import os
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))