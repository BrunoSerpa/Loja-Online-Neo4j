from re import match

def SimOuNao(resposta):
    return resposta.strip().upper() in ['S', 'N']

def NaoVazio(valor):
    return bool(valor and valor.strip())

def Numero(numero):
    return numero.isdigit()

def Email(email):
    if not email:
        return False
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return match(regex, email) is not None

def Telefone(telefone):
    return telefone.isdigit() and 8 <= len(telefone) <= 11

def Cep(cep):
    return cep.isdigit() and len(cep) == 8

def Float(numero):
    try:
        float(numero)
        return True
    except ValueError:
        return False
    
def Cpf(cpf):
    if cpf.isdigit() and len(cpf) == 11:
        def digito(cpf, posicoes):
            soma = sum(int(digito) * (posicoes + 1 - i) for i, digito in enumerate(cpf[:posicoes]))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)
        return cpf[-2] == digito(cpf, 9) and cpf[-1] == digito(cpf, 10)
    return False

def Cnpj(cnpj):
    if cnpj.isdigit() and len(cnpj) == 14:
        def Digito(cnpj, multiplicadores):
            soma = sum(int(cnpj[i]) * multiplicador for i, multiplicador in enumerate(multiplicadores))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)
        multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        multiplicadores2 = [6] + multiplicadores1
        return cnpj[-2] == Digito(cnpj, multiplicadores1) and cnpj[-1] == Digito(cnpj, multiplicadores2)
    return False