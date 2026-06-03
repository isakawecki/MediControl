from database.connection import get_connection


# Função para diminuir a quantidade do remédio após marcar como tomado
def diminuir_quantidade_remedio(remedio_id, dose):

    # Abre conexão com o banco
    cone = get_connection()

    # Cria cursor para executar SQL
    cursor = cone.cursor()

    # Diminui a quantidade do remédio, mas não deixa ficar menor que zero
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
            remedio_id
        )
    )

    # Salva alteração
    cone.commit()

    # Fecha conexão
    cone.close()