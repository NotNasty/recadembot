import dbmanager


async def adduser(bot, message):
    users_id = message.chat.id
    username = message.chat.username
    result = dbmanager.add_user(users_id, username)

    if result is not None:
        await bot.send_message(chat_id=users_id, text=result)
