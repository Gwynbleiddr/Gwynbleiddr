from db import create_connection
from sqlite3 import Connection
from conf import config


DATABASE_URL = config.get('DATABASE')


@create_connection(DATABASE_URL)
def create_tables(conn: Connection):
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                        id INTEGER PRIMARY KEY
                    )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS news_cache (
                        link TEXT PRIMARY KEY,
                        title TEXT,
                        published TEXT
                    )''')


@create_connection(DATABASE_URL)
def add_subscriber(conn: Connection, user_id):
    with conn:
        cur = conn.cursor()
        cur.execute(
            'INSERT OR IGNORE INTO subscribers (id) VALUES (?)', (user_id,))
        conn.commit()


@create_connection(DATABASE_URL)
def remove_subscriber(conn: Connection, user_id):
    with conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM subscribers WHERE id = ?', (user_id,))
        conn.commit()


@create_connection(DATABASE_URL)
def get_subscribers(conn: Connection):
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT id FROM subscribers')
        rows = cur.fetchall()
        return [row[0] for row in rows]


@create_connection(DATABASE_URL)
def add_news_to_cache(conn: Connection, news_item):
    with conn:
        cur = conn.cursor()
        cur.execute('INSERT OR IGNORE INTO news_cache (link, title, published) VALUES (?, ?, ?)',
                    (news_item['link'], news_item['title'], news_item['published']))
        conn.commit()


@create_connection(DATABASE_URL)
def get_news_cache(conn: Connection):
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT link FROM news_cache')
        rows = cur.fetchall()
        return [row[0] for row in rows]
