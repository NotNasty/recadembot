import logging
import config
import sqlite3

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


# command
@dp.message_handler(commands=["red_albums"])
async def cmd_red_albums(message: types.Message):
    await message.answer("Red Albums:")


@dp.message_handler(commands=["adduser"])
async def cmd_adduser(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CRETE TABLE IF NOT EXISTS user_id(
                   id INTEGER)
                   """)
    connect.commit()

    users_id = [message.chat.id]
    cursor.execute("INSERT INTO user_id VALUES(?);", users_id)
    connect.commit()


# echo
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
