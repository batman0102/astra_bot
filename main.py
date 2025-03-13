import logging
import asyncio
from aiogram import Bot, Dispatcher
import openai
from gpt.handlers import router
import os
from dotenv import load_dotenv
from aiogram import types

async def main():
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    openai.api_key = os.getenv('AI_TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(router) 
    await bot.set_my_commands([
        types.BotCommand(command='/start', description='Начало'),
        types.BotCommand(command='/contact', description='Контакты'),
        types.BotCommand(command='/site', description='Наш сайт'),
        types.BotCommand(command='/about', description='О нас')
    ])
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


