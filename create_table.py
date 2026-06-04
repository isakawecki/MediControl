from database.connection import get_connection


# Função responsável por criar as tabelas do banco
def init_db():

    # Abre conexão com o banco
    conn = get_connection()

    # Cria cursor para executar comandos SQL
    cursor = conn.cursor()



    # Tabela de usuários
  

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS usuarios(

            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            cpf TEXT NOT NULL UNIQUE,

            email TEXT NOT NULL UNIQUE,

            senha TEXT NOT NULL
        )

    ''')


  #tabela de remedios 

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS remedios(

            id_remedio INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            quantidade INTEGER NOT NULL,

            dose INTEGER NOT NULL,

            horario TEXT NOT NULL,

            dias_semana TEXT NOT NULL,

            estoque_minimo INTEGER NOT NULL,

            usuario_id INTEGER,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id_usuario)

        )

    ''')

    #salva alterações no banco
    conn.commit()

    #fecha conexão
    conn.close()

    print("Tabelas criadas com sucesso!")


#executa a funçao
init_db()