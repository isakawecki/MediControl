import customtkinter as ctk # importa a biblioteca usada para criar a interface gráfica
import bcrypt # importa o bcrypt para comparar a senha digitada com a senha criptografada do banco
import time # importa o time que serve para controlar o tempo de bloqueio do login
from database.connection import get_connection # importa a conexão com o banco de dados
from validacao import validar_email # importa a validação de email que foi criada em validacao.py

def abrir_tela_login():
    #guarda quantas vezes o usuário errou o login
    tentativas = 0

    #quantidade máxima de tentativas permitidas para errar a senha
    MAX_TENTATIVAS = 3

    #tempo que o login ficará bloqueado após muitas tentativas erradas
    TEMPO_BLOQUEIO = 30

    #############################################################################################################
    #função para buscar um usuário no banco pelo email
    def buscar_usuario_por_email(email):
        # Abre conexão com o banco
        
        #criando a conecão com o banco 
        cone = get_connection()

        #cria um cursor para executar comandos SQL (cursor é quem escreve os comandos no banco)
        cursor = cone.cursor()

        #busca o usuário que possui o email digitado
        #cursor fazendo isso
        cursor.execute(
            "SELECT id_usuario, nome, email, senha FROM usuarios WHERE email = ?",
            (email,)   # substitui o ? pelo email informado pelo usuário
        )

        #pega um resultado
        usuario = cursor.fetchone()

        #fecha a conexão com o banco
        cone.close()

        #retorna o usuário encontrado ou None caso não encontre
        return usuario

    ############################################################################################################
    # função chamada quando clicar no botão de login
    def fazer_login():
        #informa que vamos alterar a variável global tentativas
        nonlocal tentativas

        #limpa a mensagem de resultado antes de validar novamente
        resultado_login.configure(text="")

        # verifica se o usuário já atingiu o limite de tentativas
        if tentativas >= MAX_TENTATIVAS:

            #  mensagem de bloqueio na tela
            resultado_login.configure(
                text=f"Muitas tentativas incorretas! Aguarde {TEMPO_BLOQUEIO} segundos.",
                text_color="red"
            )

            # atualiza a interface antes de travar o sistema
            janela.update()

            # bloqueia o login por alguns segundos
            time.sleep(TEMPO_BLOQUEIO)

            # depois do bloqueio, zera as tentativas
            tentativas = 0

            # limpa a mensagem após o tempo de bloqueio
            resultado_login.configure(text="")

        # pega os valores digitados nos campos
        email = input_email.get().strip() # strip() remove espaços extras do começo e do fim
        senha = input_senha.get().strip()

        # valida se o email está correto
        if not validar_email(email):
            resultado_login.configure(
                text="Email inválido",
                text_color="red"
            )
            return

        #valida se a senha foi preenchida
        if senha == "":
            resultado_login.configure(
                text="Digite sua senha",
                text_color="red"
            )
            return

        #busca o usuário no banco pelo email
        usuario = buscar_usuario_por_email(email)

        # se não encontrou usuário, soma uma tentativa errada
        if usuario is None:
            tentativas += 1

            # calcula quantas tentativas ainda restam
            restantes = MAX_TENTATIVAS - tentativas

            resultado_login.configure(
                text=f"Email não cadastrado. Tentativas restantes: {restantes}",
                text_color="red"
            )
            return

        # se encontrou, separa os dados retornados do banco
        id_usuario, nome, email_banco, senha_hash = usuario

        #compara a senha digitada com a senha salva no banco
        senha_correta = bcrypt.checkpw(   #retorna True ou False
            senha.encode(),  #encode transforma a senha em bytes 
            senha_hash.encode() #converte o hash (senha criptografada) do banco para bytes
        )

        #see a senha estiver errada, soma uma tentativa
        if not senha_correta:
            tentativas += 1

            #calcula quantas tentativas restam
            restantes = MAX_TENTATIVAS - tentativas

            resultado_login.configure(
                text=f"Senha incorreta. Tentativas restantes: {restantes}",
                text_color="red"
            )
            return

        
        

    #se chegou aqui, o login deu certo

        # zera as tentativas erradas
        tentativas = 0

        # mensagem que deu certo 
        resultado_login.configure(
            text=f"Bem-vindo(a), {nome}!",
            text_color="green"
        )

        #atualiza a tela para  conseguir ver a mensagem
        janela.update()
        
        # Importa o arquivo de sessão.py
        import sessao

    # Salva quem é o usuário logado (la no sessao.py vai sair o none e vai ficar o id e o nome de quem logou)
        sessao.usuario_logado = id_usuario
        sessao.nome_usuario_logado = nome

    #fecha a janela do login
        janela.destroy()

    #importa e recarrega a tela principal
        # import importlib

        from gui.gui_sistema import abrir_tela_sistema
        abrir_tela_sistema()

        # importlib.reload(gui.gui_sistema)


    #################################################################################################################

    # Função para sair do login e abrir a tela de cadastro
    def ir_para_cadastro():
        # Fecha a janela atual
        janela.destroy()

        # Importa o arquivo de cadastro
        # Como o gui_cadastro.py tem janela.mainloop() no final,
        # ao importar ele, a tela de cadastro será aberta
        from gui.gui_cadastro import abrir_tela_cadastro
        abrir_tela_cadastro()
    ###################################################################################################################

    #Aqui é a configuração da interface do login - onde se usa a biblioteca customtkinter para criar as coisas
    #define o modo escuro
    ctk.set_appearance_mode("dark")


    #cria a janela principal do login
    janela = ctk.CTk()

    #define o tamanho da janela
    janela.geometry("750x600")

    #define o título
    janela.title("Login - MediControl")


    #título principal da tela
    titulo = ctk.CTkLabel(
        janela,
        text="MediControl",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=30) # pack() é quem coloca o elemento na tela e pady é o espaço em cima e embaixo 


    #texto do input email
    label_email = ctk.CTkLabel(
        janela,
        text="Email"
    )
    label_email.pack(pady=5)


    #input onde o usuário digita o email
    input_email = ctk.CTkEntry(
        janela,
        placeholder_text="Digite seu email",
        width=250
    )
    input_email.pack()


    # texto do input senha
    label_senha = ctk.CTkLabel(
        janela,
        text="Senha"
    )
    label_senha.pack(pady=5)


    # onde usuário digita a senha
    # show="*" faz a senha aparecer escondida
    input_senha = ctk.CTkEntry(
        janela,
        placeholder_text="Digite sua senha",
        show="*",
        width=250
    )
    input_senha.pack()


    #botão para fazer login
    botao_login = ctk.CTkButton(
        janela,
        text="Entrar",
        command=fazer_login
    )
    botao_login.pack(pady=20)


    # textinho que mostra erro ou sucesso no login
    resultado_login = ctk.CTkLabel(
        janela,
        text=""
    )
    resultado_login.pack(pady=5)


    #botao para ir para a tela de cadastro
    botao_cadastro = ctk.CTkButton(
        janela,
        text="Não tenho conta",
        command=ir_para_cadastro
    )
    botao_cadastro.pack(pady=10)


    #mantém a janela aberta
    janela.mainloop()
