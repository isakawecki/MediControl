from email_validator import validate_email, EmailNotValidError  #validação de email
from validate_docbr import CPF  #validação de cpf


#esse arquivo contém todas as funções de validação usadas no sistema
#ele ajuda a garantir que os dados informados pelo usuário estejam corretos


#########################################################################################

#gera um cpf válido para testes durante o desenvolvimento
cpf = CPF()
print(cpf.generate())


#########################################################################################

#essa função valida o nome informado pelo usuário
def validar_nome(nome):

    #remove espaços do começo e do final do texto
    nome = nome.strip()

    #retorna True se o nome for válido e False se for inválido
    return not (
        any(not (v.isalpha() or v.isspace()) for v in nome)
        or "  " in nome
        or len(nome.split()) < 2
    )


#########################################################################################

#essa função valida se o email está em um formato válido
def validar_email(email):

    try:

        #verifica se o email segue um formato válido
        validate_email(email)

        return True

    except EmailNotValidError:

        return False


#########################################################################################

#essa função valida se o cpf informado é válido
def validar_cpf(numero):

    #cria objeto da biblioteca de validação de cpf
    cpf = CPF()

    #remove espaços do começo e do final
    numero = numero.strip()

    #retorna True se o cpf for válido e False se for inválido
    return cpf.validate(numero)