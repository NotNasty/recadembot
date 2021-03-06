import psycopg2

HOST = "ec2-54-156-151-232.compute-1.amazonaws.com"
PASSWORD = "4ed8e454a19552618bd0aefc630573153f172f44c9685331ffddf0ae7e921eae"
DBNAME = "ddcar4vg0p8qde"
USERNAME = "wblzsehcmyhkmd"


def db_connect():
    connection = psycopg2.connect(dbname=DBNAME, user=USERNAME,
                                  password=PASSWORD, host=HOST)
    return connection


def add_user(users_id, username, first_name, last_name):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO users(id, username, first_name, last_name) VALUES({users_id}, '{username}', '{first_name}', '{last_name}');")
    except psycopg2.errors.UniqueViolation as ex:
        return 'Такой пользователь уже был добавлен в комитет'
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()
    return "Принят(-а) в комитет"


def get_all_admins():
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM users WHERE is_admin=true;")
        return cursor.fetchall()
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()


def get_all_users():
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM users;")
        return cursor.fetchall()
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()


def delete_user(user_id):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        res = cursor.execute(f"DELETE FROM users WHERE id ={user_id};")
        return cursor.fetchone()
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()


def made_admin(user_id):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE users SET is_admin = true WHERE id ={user_id};")
        return "Принят(-а) в администраторы комитета!"
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()
