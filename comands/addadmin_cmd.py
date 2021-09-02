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
admin_confirm_admin_callback = CallbackData("admin_confirm", "answer", "user_id_to_add")


# add user command
@dp.message_handler(Command("becomeadmin"))
async def cmd_start(message: types.Message):
    global admins
    global denied
    global chat
    denied = False
    chat = message.chat
    user_id = chat.id
    admins = dbmanager.get_all_admins()
    if admins:
        that_admin = list(filter(lambda admin_user: admin_user[0] == chat.id, admins))
        if that_admin:
            await bot.send_message(chat_id=user_id,
                                   text="Вы уже являетесь администратором.")
            return

        await bot.send_message(chat_id=user_id,
                               text="Подождите, пока админы комитета приймут вас в администрацию.")
        markup = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Добавить в администрацию', callback_data=admin_confirm_admin_callback.new(
            answer='add_admin', user_id_to_add=user_id))
        item_no = types.InlineKeyboardButton(text='Отклонить заявку', callback_data=admin_confirm_admin_callback.new(
            answer='not_add_amin', user_id_to_add=user_id))
        markup.add(item_yes, item_no)

        for admin in admins:
            await bot.send_message(chat_id=admin[0],
                                   text=f"Юзер {user.chat_to_string(chat)} хочет стать администратором.",
                                   reply_markup=markup, parse_mode="Markdown")
    else:
        await made_admin(message)


async def made_admin(message, user_id):
    result = dbmanager.made_admin(user_id)

    if result is not None:
        await bot.send_message(chat_id=user_id, text=result)
        if message.chat.id != user_id:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Статус заявки {user.chat_to_string(chat)} на вступление: " + result,
                                   parse_mode="Markdown")


@dp.callback_query_handler(admin_confirm_admin_callback.filter(answer='not_add_amin'))
async def admins_answer_no(call: CallbackQuery):
    user_id_to_add = call.data.split(":")[2]
    if await remove_admin_by_id(call.message.chat.id):
        await bot.send_message(chat_id=call.message.chat.id, text='Пользователь не будет добавлен в администрацию')
        global denied
        if denied is False:
            await bot.send_message(chat_id=user_id_to_add, text='Админ отклонил вашу заявку на вступление')
            denied = True


@dp.callback_query_handler(admin_confirm_admin_callback.filter(answer='add_admin'))
async def admins_answer_yes(call: CallbackQuery):
    if await remove_admin_by_id(call.message.chat.id):
        if not admins:
            if denied is False:
                user_id_to_add = call.data.split(":")[2]
                await made_admin(call.message, user_id_to_add)
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
