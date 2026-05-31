from database.connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,      
            nome TEXT NOT NULL,
            cpf  TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
''')
    conn.commit()
    conn.close()
    
    print("Tabela criada com sucesso!")

init_db()