import sqlite3


async def adduser(bot, message):
    connect = sqlite3.connect('committee.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_id(
                   id INTEGER)
                   """)
    connect.commit()

    # check if id exists
    users_id = message.chat.id
    cursor.execute(f"SELECT id FROM user_id WHERE id = {users_id}")
    data = cursor.fetchone()
    if data is None:
        # add user id
        users_id_data = [users_id]
        cursor.execute("INSERT INTO user_id VALUES(?);", users_id_data)
        connect.commit()
    else:
        await bot.send_message(users_id, 'Такой пользователь уже добвлен в комитет')