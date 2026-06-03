import customtkinter as ctk # importa a biblioteca usada para criar a interface gráfica
import sessao # importa o arquivo de sessao.py para acessar os dados do usuário que esta logado



def abrir_tela_sistema():
    #aqui tem os imports de cada função do banco que tem nessa tela
    from database.remedio import (
        salvar_remedio,
        listar_remedios,
        atualizar_remedio,
        excluir_remedio
    )

    #essa variável começa vazia porque nenhum remédio foi selecionado ainda
    #quando o usuário clicar em selecionar ela vai guardar os dados daquele remédio
    remedio_selecionado = None


    #########################################################################################

    #essa função serve para limpar todos os campos do formulário depois de alguma ação
    def limpar_campos():
        for campo in campos:
            campo.delete(0, "end")


    #########################################################################################

    #essa função pega todos os valores digitados nos inputs
    def pegar_dados():
        nome = input_nome.get().strip()
        quantidade = input_quantidade.get().strip()
        dose = input_dose.get().strip()
        horario = input_horario.get().strip()
        dias = input_dias.get().strip()
        estoque = input_estoque.get().strip()

        return nome, quantidade, dose, horario, dias, estoque


    #########################################################################################

    #essa função valida se os campos foram preenchidos corretamente
    def validar_dados(nome, quantidade, dose, horario, dias, estoque):


        #aqui ve se  falta algum campo para preencher
        if nome == "" or quantidade == "" or dose == "" or horario == "" or dias == "" or estoque == "":
            resultado.configure(text="Preencha todos os campos.")
            return False

        if not quantidade.isdigit() or not dose.isdigit() or not estoque.isdigit(): #isdigit() serve para ver se só tem numeros no campo
            resultado.configure(text="Quantidade, dose e estoque devem ser números.")
            return False

        return True


    ###########################################################################################
    #essa função mostra na tela os remedios do usuario
    def carregar_lista():

        #limpa tudo que estiver aparecendo na lista antes de atualizar ela
        for widget in frame_lista.winfo_children():
            widget.destroy()

        #busca no banco os remedios do usuario logado
        remedios = listar_remedios(sessao.usuario_logado)

        #se não tiver nenhum remedio cadastrado mostra uma mensagem
        if len(remedios) == 0:
            ctk.CTkLabel(
                frame_lista,
                text="Nenhum remédio cadastrado."
            ).pack(pady=10)
            return

        #passa por cada remedio encontrado e cria um card para ele
        for remedio in remedios:
            id_remedio, nome, quantidade, dose, horario, dias, estoque = remedio

            card = ctk.CTkFrame(frame_lista)
            card.pack(pady=8, padx=10, fill="x")

            texto = ctk.CTkLabel(
                card,
                text=(
                    f"{nome}\n"
                    f"Quantidade: {quantidade} | Dose: {dose}\n"
                    f"Horário: {horario} | Dias: {dias}\n"
                    f"Estoque mínimo: {estoque}"
                )
            )
            texto.pack(pady=5)

            ctk.CTkButton(
                card,
                text="Selecionar",
                command=lambda r=remedio: selecionar_remedio(r)
            ).pack(pady=5)


    ###########################################################################################

    #função  que coloca os dados do remédio selecionado nos campos
    def selecionar_remedio(remedio):
        nonlocal remedio_selecionado

        remedio_selecionado = remedio

        id_remedio, nome, quantidade, dose, horario, dias, estoque = remedio

        limpar_campos()

        input_nome.insert(0, nome)
        input_quantidade.insert(0, quantidade)
        input_dose.insert(0, dose)
        input_horario.insert(0, horario)
        input_dias.insert(0, dias)
        input_estoque.insert(0, estoque)

        resultado.configure(text="Remédio selecionado para edição/exclusão.")


    #########################################################################################

    #essa função salva um novo remédio no banco
    def salvar():
        nome, quantidade, dose, horario, dias, estoque = pegar_dados()

        if not validar_dados(nome, quantidade, dose, horario, dias, estoque):
            return

        salvar_remedio(
            nome,
            int(quantidade),
            int(dose),
            horario,
            dias,
            int(estoque),
            sessao.usuario_logado
        )

        resultado.configure(text="Remédio cadastrado com sucesso!")

        limpar_campos()
        carregar_lista()


    ##########################################################################
    #essa função edita o remédio que foi selecionado
    def editar():
        if remedio_selecionado is None:
            resultado.configure(text="Selecione um remédio primeiro.")
            return

        id_remedio = remedio_selecionado[0]

        nome, quantidade, dose, horario, dias, estoque = pegar_dados()

        if not validar_dados(nome, quantidade, dose, horario, dias, estoque):
            return

        atualizar_remedio(
            id_remedio,
            nome,
            int(quantidade),
            int(dose),
            horario,
            dias,
            int(estoque)
        )

        resultado.configure(text="Remédio atualizado com sucesso!")

        limpar_campos()
        carregar_lista()


    ########################################################################################

    #essa função exclui o remédio que foi selecionado
    def excluir():
        nonlocal remedio_selecionado 

        #esse if verifica se tem um remedio selecionado para excluir
        if remedio_selecionado is None:
            resultado.configure(text="Selecione um remédio primeiro.")
            return

        id_remedio = remedio_selecionado[0]

        excluir_remedio(id_remedio)

        remedio_selecionado = None

        resultado.configure(text="Remédio excluído com sucesso!")

        limpar_campos()
        carregar_lista()


    #########################################################################################

    #essa função sai do sistema e volta para o login
    def sair():
        sessao.usuario_logado = None
        sessao.nome_usuario_logado = None

        janela.destroy()

        from gui.gui_login import abrir_tela_login
        abrir_tela_login()

    #########################################################################################

    ctk.set_appearance_mode("dark")

    janela = ctk.CTk()
    janela.geometry("750x600")
    janela.title("MediControl")


    titulo = ctk.CTkLabel(
        janela,
        text="MediControl",
        font=("Arial", 30, "bold")
    )
    titulo.pack(pady=15)


    #aqui mostra o nome do usuario logado 
    usuario = ctk.CTkLabel(
        janela,
        text=f"Usuário logado: {sessao.nome_usuario_logado}"
    )
    usuario.pack(pady=5)


    frame_form = ctk.CTkFrame(janela)
    frame_form.pack(pady=10, padx=20, fill="x")



    #configurações dos inputs
    input_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome do remédio", width=300)
    input_nome.grid(row=0, column=0, padx=10, pady=5)

    input_quantidade = ctk.CTkEntry(frame_form, placeholder_text="Quantidade", width=300)
    input_quantidade.grid(row=0, column=1, padx=10, pady=5)

    input_dose = ctk.CTkEntry(frame_form, placeholder_text="Dose", width=300)
    input_dose.grid(row=1, column=0, padx=10, pady=5)

    input_horario = ctk.CTkEntry(frame_form, placeholder_text="Horário", width=300)
    input_horario.grid(row=1, column=1, padx=10, pady=5)

    input_dias = ctk.CTkEntry(frame_form, placeholder_text="Dias da semana", width=300)
    input_dias.grid(row=2, column=0, padx=10, pady=5)

    input_estoque = ctk.CTkEntry(frame_form, placeholder_text="Estoque mínimo", width=300)
    input_estoque.grid(row=2, column=1, padx=10, pady=5)


    #lista com todos os campos para facilitar na hora de limpar
    campos = [
        input_nome,
        input_quantidade,
        input_dose,
        input_horario,
        input_dias,
        input_estoque
    ]


    frame_botoes = ctk.CTkFrame(janela)
    frame_botoes.pack(pady=10)


    #botoões do CRUD e o de sair para a tela de login
    ctk.CTkButton(frame_botoes, text="Salvar", command=salvar).grid(row=0, column=0, padx=5)
    ctk.CTkButton(frame_botoes, text="Editar", command=editar).grid(row=0, column=1, padx=5)
    ctk.CTkButton(frame_botoes, text="Excluir", command=excluir).grid(row=0, column=2, padx=5)
    ctk.CTkButton(frame_botoes, text="Sair", command=sair).grid(row=0, column=3, padx=5)


    resultado = ctk.CTkLabel(janela, text="")
    resultado.pack(pady=5)


    frame_lista = ctk.CTkScrollableFrame(janela, width=680, height=270)
    frame_lista.pack(pady=10)

    #essa função é chamada assim que a tela abre, para mostrar os remedios do usuário
    carregar_lista()

    #mantem a janela aberta para o usuario conseguir mexer
    janela.mainloop()
