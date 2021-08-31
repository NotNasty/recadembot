import psycopg2

HOST = "ec2-54-156-151-232.compute-1.amazonaws.com"
PASSWORD = "4ed8e454a19552618bd0aefc630573153f172f44c9685331ffddf0ae7e921eae"
DBNAME = "ddcar4vg0p8qde"
USERNAME = "wblzsehcmyhkmd"


def db_connect():
    connection = psycopg2.connect(dbname=DBNAME, user=USERNAME,
                                  password=PASSWORD, host=HOST)
    return connection


def add_user(users_id, username):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO users(id, username) VALUES({users_id}, '{username}');")
    except psycopg2.errors.UniqueViolation as ex:
        return 'Такой пользователь уже добавлен в комитет'
    except Exception as ex:
        return ex
    conn.commit()
    cursor.close()
    conn.close()
    return "Вы приняты в комитет"


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
