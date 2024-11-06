def cep(cep):
    if not cep.isdigit():
        return cep
    if len(cep) == 8:
        return f'{cep[0:5]}-{cep[5:8]}'
    return cep

def cpf(cpf):
    if not cpf.isdigit():
        return cpf
    if len(cpf) == 11:
        return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    return cpf

def cnpj(cnpj):
    if not cnpj.isdigit():
        return cnpj
    if len(cnpj) == 14: return f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    return cnpj

def telefone(telefone):
    if not telefone.isdigit():
        return telefone
    if len(telefone) == 8:
        return f'{telefone[0:4]}-{telefone[4:8]}'
    elif len(telefone) == 9:
        return f'{telefone[0:5]}-{telefone[5:9]}'
    elif len(telefone) == 10:
        return f'({telefone[0:2]}) {telefone[2:6]}-{telefone[6:10]}'
    elif len(telefone) == 11:
        return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}'
    return telefone