from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.escolher import vendedor as escolherVendedor
from Programa.funcoes.utils.visualizar import vendedor as visualizarVendedor

from Programa.funcoes.crud import cadastrar as cadastrarVendedor, atualizar as atualizarVendedor, buscarPorAtributo, buscarTodos, excluir as excluirDado 
from Programa.funcoes.enderecos import cadastrarMultiplos as cadastrarEnderecos, gerenciar as gerenciarEnderecos
from Programa.funcoes.produtos import cadastrarMultiplos as cadastrarProdutos, gerenciar as gerenciarProdutos
from Programa.funcoes.compras import deletar as deletarVenda

def cadastrar():
    nome = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
    cnpj = entrada("Insira o CNPJ do vendedor", "Cnpj", "CNPJ inválido. deve conter apenas os 14 números.")
    email = entrada("Insira o email do vendedor", "Email", "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = entrada("Insira o telefone do vendedor", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")

    vendedor = {
        "nome_vendedor": nome,
        "cnpj": cnpj,
        "email_vendedor": email,
        "telefone_vendedor": telefone
    }

    vendedor["id"] = cadastrarVendedor("Vendedores", vendedor)
    if vendedor:
        print("Vendedor cadastrado com sucesso!")
        if entrada("Deseja cadastra seus enderecos? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não.").upper() == 'S':
            vendedor["enderecos"] = cadastrarEnderecos()
            atualizar_enderecos = atualizarVendedor("Vendedores", vendedor)
            if not atualizar_enderecos:
                return
            print("Endereços vinculados com sucesso!")

        if entrada("Deseja cadastra seus produtos? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não.").upper() == 'S':
            vendedor["produtos"] = cadastrarProdutos(vendedor)
            atualizar_produtos = atualizarVendedor("Vendedores", vendedor)
            if not atualizar_produtos:
                return
            print("Produtos vinculados com sucesso!")

def atualizar():
    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco.")
    vendedores_encontrados = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
    vendedor = escolherVendedor(vendedores_encontrados)
    if vendedor:
        while True:
            print(separador1)
            print("Vendedor atual:")
            visualizarVendedor(vendedor, True, True, True)
            print(f'{separador1}\n')

            print(separador1)
            print("O que deseja alterar?")
            print(separador2)
            print("1 - Nome")
            print("2 - CNPJ")
            print("3 - Telefone")
            print("4 - Email")
            print("5 - Enderecos")
            print("6 - Produtos")
            print(separador2)
            print("7 - Remover venda")
            print("0 - Salvar e sair")
            print(f'{separador1}\n')

            print("Qual ação deseja realizar?")
            opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma das opções!")
            limparTerminal()

            if opcaoEscolhida == '0':
                atualizar = atualizarVendedor("Vendedores", vendedor)
                if not atualizar:
                    return
                print("Vendedor atualizado com sucesso!")
                break
            elif opcaoEscolhida == '1':
                vendedor["nome_vendedor"] = entrada("Insira o novo nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
            elif opcaoEscolhida == '2':
                vendedor["cnpj"] = entrada("Insira o novo CNPJ do vendedor", "Cnpj", "CNPJ inválido. deve conter apenas os 14 números.")
            elif opcaoEscolhida == '3':
                vendedor["telefone_vendedor"] = entrada("Insira o novo telefone do vendedor", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            elif opcaoEscolhida == '4':
                vendedor["email_vendedor"] = entrada("Insira o novo email do vendedor", "Email", "Email inválido. Certifique-se de que contém '@' e '.'.")
            elif opcaoEscolhida == '5':
                vendedor["enderecos"] = gerenciarEnderecos(vendedor["enderecos"])
            elif opcaoEscolhida == '6':
                vendedor["produtos"] = gerenciarProdutos(vendedor)
            elif opcaoEscolhida == '7':
                vendedor = deletarVenda(vendedor)
            else:
                print("Opção inválida!")

def deletar():
    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco.")
    vendedores_encontrados = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
    vendedor = escolherVendedor(vendedores_encontrados)
    if vendedor:
        visualizarVendedor(vendedor, True, True, True)
        if entrada("Deseja realmente deletar este vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não.").upper() == 'S':
            if vendedor.get("enderecos"):
                for id_endereco in vendedor["enderecos"]:
                    deletar = excluirDado("Enderecos", id_endereco)
                    if not deletar:
                        return None
                print("Enderecos deletados com sucesso!")
            if vendedor.get("produtos"):
                for id_produto in vendedor["produtos"]:
                    deletar = excluirDado("Produtos", id_produto)
                    if not deletar:
                        return None
                print("Produtos deletados com sucesso!")
            deletar = excluirDado("Vendedores", vendedor['id'])
            if not deletar:
                return None
            print("Vendedor deletado com sucesso!")

def listar():
    vendedores = []
    if entrada("Deseja procurar um vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", entrada("Insira o nome do vendedor", "NaoVazio", "Insira o nome do vendedor"))    
    else:
        vendedores = buscarTodos("Vendedores")

    limparTerminal()
    if not vendedores:
        print("Nenhum vendedor encontrado!")
    elif len(vendedores) == 0:
        print("Nenhum vendedor encontrado!")
    elif len(vendedores) == 1:
        print(separador1)
        visualizarVendedor(vendedores[0], comProdutos = True, basico = True)
        print(separador1)
    else:
        for numeroVendedor, vendedor in enumerate(vendedores, start = 1):
            print(separador1)
            print(f'{numeroVendedor}º vendedor:')
            visualizarVendedor(vendedor, comProdutos = True, basico = True)
        print(separador1)