import dbmanager
from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from bot import dp, bot


admins = []
denied = False
admin_confirm_callback = CallbackData("admin_confirm", "answer")


# add user command
# @dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    global admins
    global denied
    denied = False
    users_id = message.chat.id
    username = message.chat.username
    admins = dbmanager.get_all_admins()
    if admins is not None:
        await bot.send_message(chat_id=users_id,
                               text="Подождите, пока админы комитета подтвердяд вашу заявку на вступление...")
        markup = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Добавить в комитет', callback_data=admin_confirm_callback.new(
            answer='yes'))
        item_no = types.InlineKeyboardButton(text='Отклонить заявку', callback_data=admin_confirm_callback.new(
            answer='no'))
        markup.add(item_yes, item_no)

        for admin in admins:
            await bot.send_message(chat_id=admin[0], text=f"Юзер @{username} хочет добавится в коммитет.",
                                   reply_markup=markup)
    else:
        await add_user(message)


async def add_user(message):
    result = dbmanager.add_user(users_id, username)

    if result is not None:
        await bot.send_message(chat_id=users_id, text=result)
        if message.chat.id != users_id:
            await bot.send_message(chat_id=message.chat.id, text=result)


# @dp.callback_query_handler(admin_confirm_callback.filter(answer='no'))  # lambda c: c and c.data == 'no')
async def admins_answer_no(call: CallbackQuery):
    res = await call.answer(cache_time=600)  # await  bot.answer_callback_query(callback_query_id=call.id)
    remove_admin_by_id(call.message.chat.id)
    await bot.send_message(chat_id=call.message.chat.id, text='Пользователь не будет добавлен в комитет')
    global denied
    if denied is False:
        await bot.send_message(chat_id=users_id, text='Админ отклонил вашу заявку на вступление')
        denied = True


#  @dp.callback_query_handler(admin_confirm_callback.filter(answer='yes'))  # lambda c: c and c.data == 'no')
async def admins_answer_yes(call: CallbackQuery):
    res = await call.answer(cache_time=600)  # await  bot.answer_callback_query(callback_query_id=call.id)
    remove_admin_by_id(call.message.chat.id)
    if not admins:
        if denied is False:
            await add_user(call.message)
        else:
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='К сожалению, один из администраторов уже отклонил этого участника')
    else:
        await bot.send_message(chat_id=call.message.chat.id, text='Ждем ответа остальных администраторов')


def remove_admin_by_id(admin_id):
    filtered = list(filter(lambda user: user[0] == admin_id, admins))
    if filtered:
        admins.remove(filtered[0])
