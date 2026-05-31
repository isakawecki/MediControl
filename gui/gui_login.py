import customtkinter as ctk #importa a biblioteca usada para criar a interface gráfica
import bcrypt #importa o bcrypt para comparar a senha digitada com a senha criptografada do banco
from database.connection import get_connection #Importa a conexão com o banco de dados
from validacao import validar_email #Importa a validação de email que você já tem no projeto


#Função para buscar um usuário no banco pelo email
def buscar_usuario_por_email(email):
    # Abre conexão com o banco
    cone = get_connection()

    #Cria um cursor para executar comandos SQL
    cursor = cone.cursor()

    #Busca o usuário que possui o email digitado
    cursor.execute(
        "SELECT id_usuario, nome, email, senha FROM usuarios WHERE email = ?",
        (email,)
    )

    #pega  um resultado
    usuario = cursor.fetchone()

    #fecha a conexão com o banco
    cone.close()

    #retorna o usuário encontrado ou None caso não encontre
    return usuario


#função chamada quando clicar no botão de login
def fazer_login():
    #limpa a mensagem de resultado antes de validar novamente
    resultado_login.configure(text="")

    #pega os valores digitados nos campos
    email = input_email.get().strip() #strip() remove espaços extras do começo e do fim
    senha = input_senha.get().strip()

    #valida se o email está correto (usando a função que está no validacao.py)
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

    #se não encontrou usuário, mostra erro
    if usuario is None:
        resultado_login.configure(
            text="Email não cadastrado",
            text_color="red"
        )
        return

    #se encontrou separa os dados retornados do banco
    id_usuario, nome, email_banco, senha_hash = usuario

    #compara a senha digitada com a senha salva no banco (a senha salva no banco foi criptografada, por isso o bcrypt.checkpw)
    senha_correta = bcrypt.checkpw(
        senha.encode(),
        senha_hash.encode()
    )
    # Se a senha estiver errada, mostra erro
    if not senha_correta:
        resultado_login.configure(
            text="Senha incorreta",
            text_color="red"
        )
        return
    # se o login deu certo aparece isso
    resultado_login.configure(
        text=f"Bem-vindo(a), {nome}!",
        text_color="green"
    )

    # nessa parte será adicionado o codigo para tela principal
  


# Função para sair do login e abrir a tela de cadastro
def ir_para_cadastro():
    # Fecha a janela atual 
    janela.destroy()

    #importa o arquivo de cadastro
    #como o gui_cadastro.py tem mainloop no final, ele já abre a janela  ---- arrumar isso
    import gui.gui_cadastro


#define o modo escuro da interface
ctk.set_appearance_mode("dark")

#cria a janela principal do login
janela = ctk.CTk()

#define o tamanho da janela
janela.geometry("400x500")

#define o título
janela.title("Login - MediControl")


#titulo principal da tela
titulo = ctk.CTkLabel(
    janela,
    text="MediControl",
    font=("Arial", 28, "bold")
)
titulo.pack(pady=30)


#texto ddo input email
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


#texto do input senha
label_senha = ctk.CTkLabel(
    janela,
    text="Senha"
)
label_senha.pack(pady=5)


#onde o usuário digita a senha
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


#texto que mostra erro ou sucesso no login
resultado_login = ctk.CTkLabel(
    janela,
    text=""
)
resultado_login.pack(pady=5)


#botão para ir para a tela de cadastro
botao_cadastro = ctk.CTkButton(
    janela,
    text="Não tenho conta",
    command=ir_para_cadastro
)
botao_cadastro.pack(pady=10)


#antém a janela aberta
janela.mainloop()