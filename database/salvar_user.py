import sqlite3
from database.connection import get_connection

def salvar_usuario(nome, email, cpf, senha_hash):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO usuarios (nome, email, cpf, senha) Values(?, ?, ?, ?)''', (nome, email, cpf, senha_hash))
        conn.commit()
    finally:
        conn.close()