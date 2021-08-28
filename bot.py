import logging
import config
import comands.adduser_cmd

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


# add user command
@dp.message_handler(commands=["start"])
async def cmd_adduser(message: types.Message):
    await comands.adduser_cmd.adduser(bot, message)


# echo
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
