import sqlite3
from config import DB_NAME

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# def init_db():
#     conn = get_db_connection()
#     with open('schema.sql') as f:
#         conn.executescript(f.read())
#     conn.commit()
#     conn.close()

# if __name__ == '__main__':
#     init_db()
