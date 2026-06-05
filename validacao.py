from email_validator import validate_email, EmailNotValidError #lib para validação de email
from validate_docbr import CPF #lib para vidalção de cpf


#Gerador de cpf para teste do sistema!
cpf = CPF()
print(cpf.generate()) 

# Validação de nome
def validar_nome(nome):
    nome = nome.strip() 
    return not(any(not (v.isalpha() or v.isspace()) for v in nome) or "  " in nome or len(nome.split()) < 2)


# Validação de email
def validar_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

# Validação de cpf
def validar_cpf(numero):
    cpf = CPF()
    numero = numero.strip()
    return cpf.validate(numero)
