from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.crud import fecharConexao

import Programa.funcoes.produtos as produtos
import Programa.funcoes.compras as compras
import Programa.funcoes.vendedores as vendedores
import Programa.funcoes.usuarios as usuarios

def menuExibido(titulo, opcoes, textoVoltar = 'Voltar'):
    while True:
        print(separador1)
        print(titulo)
        print(separador2)
        for numeroAcao, opcao in enumerate(opcoes, start = 1):
            print(f'{numeroAcao} - {opcao["descricao"]}')
        print(separador2)
        print(f'0 - {textoVoltar}')
        print(separador1)
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção","Numero", "Insira uma das opções!")
        limparTerminal()
        if opcaoEscolhida == '0':
            if textoVoltar != 'Voltar':
                fecharConexao()
            break
        try:
            opcaoIndex = int(opcaoEscolhida) - 1
            if 0 <= opcaoIndex < len(opcoes):
                opcoes[opcaoIndex]["acao"]()
            else: print("Opção inválida!")
        except ValueError: print("Opção inválida!")

def menuUsuario():
    opcoes = [
        {"descricao": "Cadastar usuario", "acao": usuarios.cadastrar},
        {"descricao": "Listar usuarios", "acao": usuarios.listar},
        {"descricao": "Atualizar usuario", "acao": usuarios.atualizar},
        {"descricao": "Deletar usuario", "acao": usuarios.deletar}
    ]
    menuExibido("Gerenciar Usuários", opcoes)

def menuVendedor():
    opcoes = [
        {"descricao": "Cadastar vendedor", "acao": vendedores.cadastrar},
        {"descricao": "Listar vendedores", "acao": vendedores.listar},
        {"descricao": "Atualizar vendedor", "acao": vendedores.atualizar},
        {"descricao": "Deletar vendedor", "acao": vendedores.deletar}
    ]
    menuExibido("Gerenciar Vendedores", opcoes)

def menuProduto():
    opcoes = [
        {"descricao": "Cadastar produto", "acao": produtos.cadastrar},
        {"descricao": "Listar produtos", "acao": produtos.listar},
        {"descricao": "Atualizar produto", "acao": produtos.atualizar},
        {"descricao": "Deletar produto", "acao": produtos.deletar}
    ]
    menuExibido("Gerenciar Produtos", opcoes)

def menuCompra():
    opcoes = [
        {"descricao": "Cadastar compra", "acao": compras.cadastrar},
        {"descricao": "Deletar compra", "acao": compras.deletar},
        {"descricao": "Listar compras", "acao": compras.listarCompras},
        {"descricao": "Listar vendas", "acao": compras.listarVendas},
    ]
    menuExibido("Gerenciar Compras", opcoes)

def home():
    opcoes = [
        {"descricao": "Gerenciar Usuarios", "acao": menuUsuario},
        {"descricao": "Gerenciar Vendedores", "acao": menuVendedor},
        {"descricao": "Gerenciar Produtos", "acao": menuProduto},
        {"descricao": "Gerenciar Compras", "acao": menuCompra}
    ]
    menuExibido("Menu Principal", opcoes, textoVoltar = "Sair do Sistema")