from database.connection import get_connection


# salva um novo remédio no banco
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


# lista só os remédios do usuário logado
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

    remedios = cursor.fetchall()
    conn.close()

    return remedios


# atualiza um remédio já cadastrado
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


# apaga um remédio pelo id
def excluir_remedio(id_remedio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM remedios WHERE id_remedio = ?",
        (id_remedio,)
    )

    conn.commit()
    conn.close()