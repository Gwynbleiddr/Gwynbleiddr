from functools import wraps
import sqlite3


def create_connection(db_file):
    def decorator(func):
        wraps(func)

        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db_file)
            return func(conn, *args, **kwargs)

        return wrapper

    return decorator

