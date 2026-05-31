import customtkinter as ctk #lib para interface gráfica
from database.salvar_user import salvar_usuario #importação da função para salvar usuario no banco
from validacao import validar_nome, validar_email, validar_cpf #importação das funções de validações
import bcrypt #lib para encryptar senha
import re #lib de expressão regular para validações
import sqlite3 #importação do sqlite


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

# aparência da janela
ctk.set_appearance_mode('dark')

# Definindo a janela
janela = ctk.CTk()

# Tamanho da janela
janela.geometry("400x700")

# Titulo da janela
janela.title("Cadastro")

# Label nome
label_nome = ctk.CTkLabel(janela, text='Nome')
label_nome.pack(pady=5)

# Campo de entrada do nome
input_nome = ctk.CTkEntry(janela,placeholder_text='Digite seu nome')
input_nome.pack()

# Campo da mensagem de erro ou sucesso
resultado_nome = ctk.CTkLabel(janela, text='')
resultado_nome.pack()

# Label email
label_email = ctk.CTkLabel(janela, text='Email')
label_email.pack(pady=5)

# Campo de entrada do email
input_email = ctk.CTkEntry(janela,placeholder_text='Digite seu email')
input_email.pack()

# Campo da mensagem de erro ou sucesso
resultado_email = ctk.CTkLabel(janela, text='')
resultado_email.pack()

# Label cpf
label_cpf = ctk.CTkLabel(janela, text='CPF')
label_cpf.pack(pady=5)

# Campo de entrada do cpf
input_cpf = ctk.CTkEntry(janela,placeholder_text='Digite seu cpf')
input_cpf.pack()

# Campo da mensagem de erro ou sucesso
resultado_cpf = ctk.CTkLabel(janela, text='')
resultado_cpf.pack()

# Label senha
label_senha = ctk.CTkLabel(janela, text='Senha')
label_senha.pack(pady=5)

# Campo de entrada da senha
input_senha = ctk.CTkEntry(janela,placeholder_text='Digite sua senha',show="*")
input_senha.pack()

# Campo da mensagem de erro ou sucesso
resultado_senha = ctk.CTkLabel(janela, text='')
resultado_senha.pack()

# botão
botao_cadastro = ctk.CTkButton(
janela,text='Cadastrar-se', command=cadastrar) #Instanciando a funcao cadastrar

botao_cadastro.pack(pady=20)

# resultado do cadastro
resultado_cadastro = ctk.CTkLabel(janela, text='')
resultado_cadastro.pack()

# deixar a janela rodando
janela.mainloop()