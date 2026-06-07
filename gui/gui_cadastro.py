import customtkinter as ctk 
from database.user import salvar_usuario #importação da função para salvar usuario no banco
from validacao import validar_nome, validar_email, validar_cpf #importação das funções de validações
import bcrypt #lib para encryptar senha
import re #lib de expressão regular para validações
import sqlite3 #importação do sqlite


##################################################################################

def abrir_tela_cadastro():
   
   ############################################
    #função para ir para a tela de login
    def ir_para_login():

        #fecha a janela atual do cadastro
        janela.destroy()

        #import do arquivo de login
        from gui.gui_login import abrir_tela_login
        abrir_tela_login()
    ################################################
    def cadastrar():
        #Escopo para resultado dos inputs, nome válido, nome inválido, etc
        resultado_nome.configure(text='')
        resultado_email.configure(text='')
        resultado_cpf.configure(text='')
        resultado_senha.configure(text='')
        resultado_cadastro.configure(text='')

        #Pegar os dados digitados nos inputs
        nome = input_nome.get()
        email = input_email.get()
        cpf = input_cpf.get()
        senha = input_senha.get().strip() #remover espaços da senha

        erro = False #Variavel usada para verificar erros, começando em false, 0 erros existentes

        # valida nome
        if not validar_nome(nome):
            resultado_nome.configure(text='Nome inválido', text_color='red')
            erro = True

        # valida email
        if not validar_email(email):
            resultado_email.configure(text='Email inválido', text_color='red')
            erro = True

        # valida cpf
        if not validar_cpf(cpf):
            resultado_cpf.configure(text='CPF inválido',text_color='red')
            erro = True

        # valida senha
        if len(senha) < 6:
            resultado_senha.configure(text='Mínimo 6 caracteres', text_color='red')
            erro = True

        elif not re.search(r"[A-Z]", senha):
            resultado_senha.configure(text='Falta letra maiúscula',text_color='red')
            erro = True

        elif not re.search(r"[a-z]", senha):
            resultado_senha.configure(text='Falta letra minúscula',text_color='red')
            erro = True

        elif not re.search(r"[0-9]", senha):
            resultado_senha.configure(text='Falta número',text_color='red')
            erro = True

        elif not re.search(r"[!@#$%&*]", senha):
            resultado_senha.configure(text='Falta caractere especial',text_color='red')
            erro = True

        # se tiver algum erro para aqui
        if erro:
            return

        # gera senha hash
        senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt()).decode()

        # salva no banco
        try:
            salvar_usuario(nome, email, cpf, senha_hash)
            resultado_cadastro.configure(text='Usuário cadastrado com sucesso!',text_color='green')

        except sqlite3.IntegrityError:
            resultado_cadastro.configure(text='CPF ou Email já cadastrado!',text_color='red')

        except Exception:
            resultado_cadastro.configure(text='Ocorreu um erro inesperado!',text_color='red')

   ############################################################################################# 
    
     #Area de edição da aparência da janela, tamanho, título, etc
     
    # aparência da janela
    ctk.set_appearance_mode('dark')

    # Definindo a janela
    janela = ctk.CTk()

    # Tamanho da janela
    janela.geometry("750x670")

    # Titulo da janela
    janela.title("MediControl")

    # Configura a coluna para centralizar tudo horizontalmente
    janela.grid_columnconfigure(0, weight=1)
    
    # Título Principal
    titulo = ctk.CTkLabel(
        janela,
        text="Cadastro",
        font=("Arial", 28, "bold")
    )
    titulo.grid(row=0, column=0, pady=(50, 30), sticky="nsew")
    
    # BLOCO NOME 
    label_nome = ctk.CTkLabel(janela, text='Nome')
    label_nome.grid(row=1, column=0, padx=250, pady=(5, 2), sticky="w") 

    input_nome = ctk.CTkEntry(janela, placeholder_text='Digite seu nome', width=250)
    input_nome.grid(row=2, column=0, padx=250, pady=(0, 2))

    resultado_nome = ctk.CTkLabel(janela, text='', font=("Arial", 11))
    resultado_nome.grid(row=3, column=0, pady=(0, 5))

    #BLOCO EMAIL 
    label_email = ctk.CTkLabel(janela, text='Email')
    label_email.grid(row=4, column=0, padx=250, pady=(5, 2), sticky="w") 

    input_email = ctk.CTkEntry(janela, placeholder_text='Digite seu email', width=250)
    input_email.grid(row=5, column=0, padx=250, pady=(0, 2))

    resultado_email = ctk.CTkLabel(janela, text='', font=("Arial", 11))
    resultado_email.grid(row=6, column=0, pady=(0, 5))

    #BLOCO CPF
    label_cpf = ctk.CTkLabel(janela, text='CPF')
    label_cpf.grid(row=7, column=0, padx=250, pady=(5, 2), sticky="w") 

    input_cpf = ctk.CTkEntry(janela, placeholder_text='Digite seu cpf', width=250)
    input_cpf.grid(row=8, column=0, padx=250, pady=(0, 2))

    resultado_cpf = ctk.CTkLabel(janela, text='', font=("Arial", 11))
    resultado_cpf.grid(row=9, column=0, pady=(0, 5))

    #BLOCO SENHA 
    label_senha = ctk.CTkLabel(janela, text='Senha')
    label_senha.grid(row=10, column=0, padx=250, pady=(5, 2), sticky="w") 

    input_senha = ctk.CTkEntry(janela, placeholder_text='Digite sua senha', show="*", width=250)
    input_senha.grid(row=11, column=0, padx=250, pady=(0, 2))

    resultado_senha = ctk.CTkLabel(janela, text='', font=("Arial", 11))
    resultado_senha.grid(row=12, column=0, pady=(0, 10))

    #RESULTADO DO CADASTRO (usuário cadastrado, cpf ou email já cadastrado, erro inesperado, etc)
    resultado_cadastro = ctk.CTkLabel(janela, text='', font=("Arial", 12, "bold"))
    resultado_cadastro.grid(row=13, column=0, pady=5)

    #BOTÃO CADASTRAR 
    botao_cadastro = ctk.CTkButton(
        janela, 
        text='Cadastrar-se', 
        width=250, 
        height=35, 
        font=("Arial", 14, "bold"),
        command=cadastrar
    )
    botao_cadastro.grid(row=14, column=0, pady=(5, 5))

    #BOTÃO VOLTAR LOGAR 
    botao_login = ctk.CTkButton(
        janela,                 
        text="Já tenho conta",   
        fg_color="transparent",
        text_color="#1f538d",
        hover_color="#242424",
        command=ir_para_login 
    )
    botao_login.grid(row=15, column=0, pady=(5, 15))

    #mantém a janela aberta
    janela.mainloop()