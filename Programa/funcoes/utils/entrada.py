from Programa.funcoes.utils.salvarErro import salvarErro
import Programa.funcoes.utils.validar as validar

def entrada(mensagem, validacao, erroMensagem):
    validacoes = [attr for attr in dir(validar) if callable(getattr(validar, attr)) and not attr.startswith('__')]
    
    if validacao not in validacoes:
        salvarErro(
            "Erro ao buscar validação", 
            f"A função de validação '{validacao}' não existe no módulo 'validar'. Funções disponíveis: {', '.join(validacoes)}"
        )
        return None

    valido = getattr(validar, validacao)

    while True:
        entrada = input(f'{mensagem}: ')
        if not valido(entrada):
            print(erroMensagem)
        else:
            return entrada