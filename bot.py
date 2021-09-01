from loader import bot


async def on_shutdown(dispatcher):
    await bot.close()

if __name__ == '__main__':
    from aiogram import executor
    from comands import dp
    executor.start_polling(dp, skip_updates=True)
