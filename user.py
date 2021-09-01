from aiogram import types


def chat_to_string(chat: types.Chat):
    if chat.username == 'None':
        return f"@{chat.username}({chat.first_name} {chat.last_name})"
    else:
        return f"[{chat.first_name} {chat.last_name}](tg://user?id={str(chat.id)})"
