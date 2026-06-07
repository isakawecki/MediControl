from database.connection import get_connection


#esse arquivo é responsável pelas operações relacionadas aos usuários
#ele cria a tabela de usuários e também salva novos usuários no banco


#########################################################################################

#essa função cria a tabela de usuários no banco de dados
def criar_tabela_usuarios():

    #abre conexão com o banco
    conn = get_connection()

    #cria cursor para executar comandos SQL
    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS usuarios(

            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            cpf TEXT NOT NULL UNIQUE,

            email TEXT NOT NULL UNIQUE,

            senha TEXT NOT NULL
        )

    ''')

    #salva alterações no banco
    conn.commit()

    #fecha conexão
    conn.close()


#########################################################################################

#essa função salva um novo usuário no banco de dados
def salvar_usuario(nome, email, cpf, senha_hash):

    #abre conexão com o banco
    conn = get_connection()

    #cria cursor para executar comandos SQL
    cursor = conn.cursor()

    try:

        #insere os dados do usuário na tabela usuarios
        cursor.execute(
            '''
            INSERT INTO usuarios
            (nome, email, cpf, senha)
            VALUES (?, ?, ?, ?)
            ''',
            (nome, email, cpf, senha_hash)
        )

        #salva alterações no banco
        conn.commit()
    #o finally executa sempre, então garante que a conexão será fechada mesmo que aconteça algum erro
    finally:

        #fecha conexão mesmo que aconteça algum erro
        conn.close()