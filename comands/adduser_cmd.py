import dbmanager
import user
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from loader import dp, bot

chat = None
admins = []
denied = False
admin_confirm_callback = CallbackData("admin_confirm", "answer", "user_id_to_add", "username_to_add")


# add user command
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    global admins
    global denied
    global chat
    denied = False
    chat = message.chat
    user_id = chat.id
    admins = dbmanager.get_all_admins()
    if admins:
        await bot.send_message(chat_id=user_id,
                               text="Подождите, пока админы комитета подтвердят вашу заявку на вступление...")
        markup = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Добавить в комитет', callback_data=admin_confirm_callback.new(
            answer='yes', user_id_to_add=user_id, username_to_add=chat.username))
        item_no = types.InlineKeyboardButton(text='Отклонить заявку', callback_data=admin_confirm_callback.new(
            answer='no', user_id_to_add=user_id, username_to_add=chat.username))
        markup.add(item_yes, item_no)

        for admin in admins:
            await bot.send_message(chat_id=admin[0],
                                   text=f"Юзер {user.chat_to_string(chat)} хочет вступить в коммитет.",
                                   reply_markup=markup, parse_mode="Markdown")
    else:
        await add_user(message, user_id, chat.username)


async def add_user(message, user_id, username):
    result = dbmanager.add_user(user_id, username, chat.first_name, chat.last_name)

    if result is not None:
        await bot.send_message(chat_id=user_id, text=result)
        if message.chat.id != user_id:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Статус заявки {user.chat_to_string(chat)} на вступление: " + result,
                                   parse_mode="Markdown")


@dp.callback_query_handler(admin_confirm_callback.filter(answer='no'))
async def admins_answer_no(call: CallbackQuery):
    await call.answer(cache_time=600)
    user_id_to_add = call.data.split(":")[2]
    if await remove_admin_by_id(call.message.chat.id):
        await bot.send_message(chat_id=call.message.chat.id, text='Пользователь не будет добавлен в комитет')
        global denied
        if denied is False:
            await bot.send_message(chat_id=user_id_to_add, text='Админ отклонил вашу заявку на вступление')
            denied = True


@dp.callback_query_handler(admin_confirm_callback.filter(answer='yes'))
async def admins_answer_yes(call: CallbackQuery):
    await call.answer(cache_time=600)
    if await remove_admin_by_id(call.message.chat.id):
        if not admins:
            if denied is False:
                user_id_to_add = call.data.split(":")[2]
                username_to_add = call.data.split(":")[3]
                await add_user(call.message, user_id_to_add, username_to_add)
            else:
                await bot.send_message(chat_id=call.message.chat.id,
                                       text='К сожалению, один из администраторов уже отклонил этого участника')
        else:
            await bot.send_message(chat_id=call.message.chat.id, text='Ждем ответа остальных администраторов')


async def remove_admin_by_id(admin_id):
    filtered = list(filter(lambda admin_user: admin_user[0] == admin_id, admins))
    if filtered:
        admins.remove(filtered[0])
        return True
    else:
        await bot.send_message(chat_id=admin_id,
                               text='Вы уже приняли решение по поводу этого участника, нельзя переголосовать')
        return False
