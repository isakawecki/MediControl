from database.connection import get_connection
from datetime import date
import sessao


#esse arquivo é responsável por tudo que envolve os remédios
#ele cria as tabelas e também faz as operações de cadastrar,
#listar, editar, excluir e controlar quando o remédio foi tomado


#########################################################################################

#essa função cria a tabela de remédios no banco de dados
def criar_tabela_remedios():

    #abre conexão com o banco
    conn = get_connection()

    #cria cursor para executar comandos SQL
    cursor = conn.cursor()

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

    #salva alterações
    conn.commit()

    #fecha conexão
    conn.close()


#########################################################################################

#essa função cria a tabela que guarda quando o usuário marcou um remédio como tomado
def criar_tabela_historico():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS historico(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_usuario INTEGER NOT NULL,

            id_remedio INTEGER NOT NULL,

            data TEXT NOT NULL,

            status TEXT NOT NULL,

            FOREIGN KEY (id_usuario)
            REFERENCES usuarios(id_usuario),

            FOREIGN KEY (id_remedio)
            REFERENCES remedios(id_remedio)

        )

    ''')

    conn.commit()
    conn.close()


#########################################################################################

#salva um novo remédio no banco
def salvar_remedio(nome, quantidade, dose, horario, dias, estoque_minimo, usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO remedios
        (nome, quantidade, dose, horario, dias_semana, estoque_minimo, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nome, quantidade, dose, horario, dias, estoque_minimo, usuario_id)
    )

    conn.commit()
    conn.close()


#########################################################################################

#lista todos os remédios do usuário logado
def listar_remedios(usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_remedio, nome, quantidade, dose, horario, dias_semana, estoque_minimo
        FROM remedios
        WHERE usuario_id = ?
        """,
        (usuario_id,)
    )

    #pega todos os registros encontrados
    remedios = cursor.fetchall()

    conn.close()

    return remedios


#########################################################################################

#atualiza as informações de um remédio já cadastrado
def atualizar_remedio(id_remedio, nome, quantidade, dose, horario, dias, estoque_minimo):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE remedios
        SET nome = ?, quantidade = ?, dose = ?, horario = ?, dias_semana = ?, estoque_minimo = ?
        WHERE id_remedio = ?
        """,
        (nome, quantidade, dose, horario, dias, estoque_minimo, id_remedio)
    )

    conn.commit()
    conn.close()


#############################################################################################

#remove um remédio do banco pelo id
def excluir_remedio(id_remedio):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM remedios WHERE id_remedio = ?",
        (id_remedio,)
    )

    conn.commit()
    conn.close()


#########################################################################################

#verifica se o usuário já marcou aquele remédio como tomado hoje
#isso impede que o botão "Tomei Hoje" seja usado várias vezes no mesmo dia
def ja_tomou_hoje(id_remedio):

    conn = get_connection()
    cursor = conn.cursor()

    #pega a data atual
    data_hoje = date.today().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT id
        FROM historico
        WHERE id_usuario = ?
        AND id_remedio = ?
        AND data = ?
        AND status = ?
        """,
        (
            sessao.usuario_logado,
            id_remedio,
            data_hoje,
            "Tomou"
        )
    )

    registro = cursor.fetchone()

    conn.close()

    #retorna True se encontrou registro e False se não encontrou
    return registro is not None


################################################################################

#salva no histórico que o usuário tomou o remédio hoje
def salvar_historico_tomou(id_remedio):

    conn = get_connection()
    cursor = conn.cursor()

    data_hoje = date.today().strftime("%Y-%m-%d")

    cursor.execute(
        """
        INSERT INTO historico
        (id_usuario, id_remedio, data, status)
        VALUES (?, ?, ?, ?)
        """,
        (
            sessao.usuario_logado,
            id_remedio,
            data_hoje,
            "Tomou"
        )
    )

    conn.commit()
    conn.close()


######################################################################################

#diminui a quantidade do remédio no estoque
#essa função é chamada quando o usuário marca "Tomei Hoje"
def diminuir_estoque(id_remedio, dose):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE remedios
        SET quantidade =
            CASE
                WHEN quantidade - ? < 0 THEN 0
                ELSE quantidade - ?
            END
        WHERE id_remedio = ?
        """,
        (
            dose,
            dose,
            id_remedio
        )
    )

    conn.commit()
    conn.close()