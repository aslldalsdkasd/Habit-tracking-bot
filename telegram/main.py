import os
import asyncio
from .init_bot import bot
from .handlers.command import *

async def main():
    await bot.polling(non_stop=True)


if __name__ == '__main__':
    print("start")
    asyncio.run(main())