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
admin_confirm_callback = CallbackData("admin_confirm", "answer")


# add user command
@dp.message_handler(Command("deleteuser"))
async def cmd_deleteuser(message: types.Message):
    # message.answer(text=f"Введите ссылку на участника (ссылка начинается с @)")
    # message.text.__contains__("@")
    global admins
    global denied
    global chat
    denied = False
    chat = message.chat
    users_id = chat.id
    admins = dbmanager.get_all_admins()

    if admins:
        that_admin = list(filter(lambda admin_user: admin_user[0] == chat.id, admins))
        if that_admin:
            await bot.send_message(chat_id=users_id,
                                   text="Подождите, пока админы комитета подтвердят удаление этого участника.")
            markup = types.InlineKeyboardMarkup()
            delete_yes = types.InlineKeyboardButton(text='Подтвердить удаление',
                                                    callback_data=admin_confirm_callback.new(
                                                        answer='delete'))
            delete_no = types.InlineKeyboardButton(text='Не надо удалять!', callback_data=admin_confirm_callback.new(
                answer='not_delete'))
            markup.add(delete_yes, delete_no)

            for admin in admins:
                if admin is not that_admin:
                    await bot.send_message(chat_id=admin[0],
                                           text=f"Aдмин {user.chat_to_string(chat)} хочет вступить в коммитет.",
                                           reply_markup=markup)
        else:
            await bot.send_message(chat_id=users_id, text="Вы не являетесь администратором комитета.")
    else:
        await add_user(message)


async def add_user(user_id):
    result = dbmanager.delete_user(user_id)  # .add_user(chat.id, chat.username, chat.first_name, chat.last_name)

    if result is not None:
        await bot.send_message(chat_id=chat.id, text=result)
        await bot.send_message(chat_id=user_id,
                               text=f"Статус заявки {user.chat_to_string(chat)} на вступление: " + result)


@dp.callback_query_handler(admin_confirm_callback.filter(answer='not_delete'))  # lambda c: c and c.data == 'no')
async def admins_answer_no(call: CallbackQuery):
    if await remove_admin_by_id(call.message.chat.id):
        await bot.send_message(chat_id=call.message.chat.id, text='Пользователь не будет добавлен в комитет')
        global denied
        if denied is False:
            await bot.send_message(chat_id=chat.id, text='Админ отклонил вашу заявку на вступление')
            denied = True


@dp.callback_query_handler(admin_confirm_callback.filter(answer='delete'))  # lambda c: c and c.data == 'no')
async def admins_answer_yes(call: CallbackQuery):
    if await remove_admin_by_id(call.message.chat.id):
        if not admins:
            if denied is False:
                await add_user(call.message)
            else:
                await bot.send_message(chat_id=call.message.chat.id,
                                       text='К сожалению, один из администраторов уже отклонил этого участника')
        else:
            await bot.send_message(chat_id=call.message.chat.id, text='Ждем ответа остальных администраторов')


async def remove_admin_by_id(admin_id):
    filtered = list(filter(lambda the_admin: the_admin[0] == admin_id, admins))
    if filtered:
        admins.remove(filtered[0])
        return True
    else:
        await bot.send_message(chat_id=admin_id,
                               text='Вы уже приняли решение по поводу этого участника, нельзя переголосовать')
        return False
