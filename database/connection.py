import sqlite3

DB_PATH = "database/banco.db"

def get_connection():
    return sqlite3.connect(DB_PATH)