from database.user import criar_tabela_usuarios
from database.remedio import criar_tabela_remedios, criar_tabela_historico


#esse arquivo serve para criar todas as tabelas do banco de dados
#ele chama as funções que estão nos arquivos user.py e remedio.py
#assim toda a criação das tabelas fica centralizada em um único lugar


#função responsável por criar todas as tabelas necessárias para o sistema funcionar
def init_db():

    #cria a tabela de usuários
    criar_tabela_usuarios()

    #cria a tabela de remédios
    criar_tabela_remedios()

    #cria a tabela de histórico de utilização dos remédios
    criar_tabela_historico()

    #mensagem exibida quando todas as tabelas forem criadas com sucesso
    print("Tabelas criadas com sucesso!")


#executa a função automaticamente quando esse arquivo for iniciado
init_db()