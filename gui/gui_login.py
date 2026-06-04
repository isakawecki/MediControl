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
    # FUNÇÃO AUXILIAR executa a contagem regressiva na tela 
    def atualizar_contagem_bloqueio(tempo_restante):
        # Atualiza o texto com o tempo descendo de 1 em 1 segundo
        nonlocal tentativas

        if tempo_restante > 0:
            #  mensagem de bloqueio na tela
            resultado_login.configure(
                text=f"Muitas tentativas incorretas! Aguarde {tempo_restante} segundos.",
                text_color="red"
            )
            # Execução da função para daqui a 1000ms (1 segundo) passando o tempo reduzido
            janela.after(1000, atualizar_contagem_bloqueio, tempo_restante - 1)
        else:
            # O tempo acabou zera os erros, limpa as mensagens e reativa os botões do sistema
            tentativas = 0
            resultado_login.configure(text="")
            botao_login.configure(state="normal")
            botao_cadastro.configure(state="normal")

    # função chamada quando clicar no botão de login
    def fazer_login():
        #informa que vamos alterar a variável global tentativas
        nonlocal tentativas

        #limpa a mensagem de resultado antes de validar novamente
        resultado_login.configure(text="")

        # verifica se o usuário já atingiu o limite de tentativas
        if tentativas >= MAX_TENTATIVAS:
            # Desativa os botões para o usuário não conseguir clicar durante o bloqueio
            botao_login.configure(state="disabled")
            botao_cadastro.configure(state="disabled")
            
            # Inicia o relógio regressivo começando em 30 segundos
            atualizar_contagem_bloqueio(30)
            return
           

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
            restantes = MAX_TENTATIVAS - tentativas

            if tentativas >= MAX_TENTATIVAS:
                botao_login.configure(state="disabled")
                botao_cadastro.configure(state="disabled")
                atualizar_contagem_bloqueio(30)
            else:
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

        #se a senha estiver errada, soma uma tentativa
        if not senha_correta:
            tentativas += 1
            restantes = MAX_TENTATIVAS - tentativas

            if tentativas >= MAX_TENTATIVAS:
                botao_login.configure(state="disabled")
                botao_cadastro.configure(state="disabled")
                atualizar_contagem_bloqueio(30)
            else:
                resultado_login.configure(
                    text=f"Senha incorreta. Tentativas restantes: {restantes}",
                    text_color="red"
                )
            return

        # se chegou aqui, o login deu certo
        tentativas = 0

        resultado_login.configure(
            text=f"Bem-vindo(a), {nome}!",
            text_color="green"
        )

        janela.update()
        
        import sessao
        sessao.usuario_logado = id_usuario
        sessao.nome_usuario_logado = nome

        janela.destroy()

        from gui.gui_sistema import abrir_tela_sistema
        abrir_tela_sistema()


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

    #define o modo escuro
    ctk.set_appearance_mode("dark")


    #cria a janela principal do login
    janela = ctk.CTk()

    #define o tamanho da janela
    janela.geometry("750x600")

    #define o título
    janela.title("MediControl")

    # Configura as colunas da janela para centralizar o conteúdo
    janela.grid_columnconfigure(0, weight=1)

    # 1. Título principal da tela
    titulo = ctk.CTkLabel(
        janela,
        text="Login",
        font=("Arial", 28, "bold")
    )
    titulo.grid(row=0, column=0, pady=(50, 30), sticky="nsew") # row=0: Primeira linha da tela


    # 2. Texto do input email (Alinhado à esquerda)
    label_email = ctk.CTkLabel(
        janela,
        text="Email",
        font=("Arial", 14)
    )
    label_email.grid(row=1, column=0, padx=250, pady=(10, 2), sticky="w") 
    # row=1 | sticky="w" joga o texto para a esquerda (West).
    # padx=250 serve para alinhar o início do texto com o início do input de largura 250


    # 3. Input onde o usuário digita o email
    input_email = ctk.CTkEntry(
        janela,
        placeholder_text="Digite seu email",
        width=250
    )
    input_email.grid(row=2, column=0, padx=250, pady=(0, 15)) # row=2


    # 4. Texto do input senha (Alinhado à esquerda)
    label_senha = ctk.CTkLabel(
        janela,
        text="Senha",
        font=("Arial", 14)
    )
    label_senha.grid(row=3, column=0, padx=250, pady=(10, 2), sticky="w") # row=3 | sticky="w" joga para a esquerda


    # 5. Onde o usuário digita a senha
    # show="*" faz a senha aparecer escondida
    input_senha = ctk.CTkEntry(
        janela,
        placeholder_text="Digite sua senha",
        show="*",
        width=250
    )
    input_senha.grid(row=4, column=0, padx=250, pady=(0, 5)) # row=4

    # 6. Textinho que mostra erro ou sucesso no login (Fica logo abaixo da senha)
    resultado_login = ctk.CTkLabel(
        janela,
        text=""
    )
    resultado_login.grid(row=5, column=0, pady=5) # row=5

    # 7. Botão para fazer login
    botao_login = ctk.CTkButton(
        janela,
        text="Entrar",
        width=250,
        height=40,
        font=("Arial", 15, "bold"),
        command=fazer_login
    )
    botao_login.grid(row=6, column=0, pady=(15, 10)) # row=6




    # 8. Botão para ir para a tela de cadastro
    botao_cadastro = ctk.CTkButton(
        janela,
        text="Não tenho conta",
        fg_color="transparent", #Remove o fundo azul dele
        text_color="#1f538d", #Deixa o texto com a cor azul padrão
        hover_color="#242424",#Cor de fundo suave quando passa o mouse por cima
        command=ir_para_cadastro
    )
    botao_cadastro.grid(row=7, column=0, pady=10) #row=7


    #mantém a janela aberta
    janela.mainloop()
