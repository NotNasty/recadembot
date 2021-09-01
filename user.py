from aiogram import types


def chat_to_string(chat: types.Chat):
    if chat.username is not 'None':
        return f"@{chat.username}({chat.first_name} {chat.last_name})"
    else:
        return f"{chat.first_name} {chat.last_name}"
