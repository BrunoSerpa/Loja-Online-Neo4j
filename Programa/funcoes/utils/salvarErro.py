from logging import basicConfig, error, ERROR

def configurarLog():
    basicConfig(
        filename='erros.log',
        level=ERROR,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

def salvarErro(descricao, erro):
    error(f"{descricao}. Detalhes: {erro}")

configurarLog()