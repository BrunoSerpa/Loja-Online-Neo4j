from Programa.funcoes.crud import cadastrar as cadastrarProduto, atualizar as atualizarDado, excluir as excluirProduto, buscarPorAtributo, buscarPorId, buscarTodos
from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import vendedor as escolherVendedor, produto as escolherProduto
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.visualizar import produto as visualizarProduto

def cadastrar(vendedor = None):
    comVendedor = False if vendedor == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherVendedor(vendedores)
        if not vendedor:
            return None

    nome = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco")
    valor = float(entrada("Insira o valor do produto (exemplo: 1.23)", "Float", 'Valor Inválido. Deve conter apenas o número decimal, separando por ".".'))

    produto = {
        "nome_produto": nome,
        "valor_produto": valor,
        "id_vendedor" : vendedor.get("id")
    }

    id = cadastrarProduto("Produtos", produto)
    if not id:
        return None

    print("Produto cadastrado com sucesso!")
    if not comVendedor:
        if not vendedor.get("produtos"):
            vendedor["produtos"] = []
        vendedor["produtos"].append(id)
        atualizar = atualizarDado("Vendedores", vendedor)

        if not atualizar:
            excluirProduto("Produtos", id)
            return None
        print("Vendedor vinculado com sucesso!")
    return id
   
def cadastrarMultiplos(vendedor):
    produtos = []
    while True:
        limparTerminal()
        produto = cadastrar(vendedor)
        if produto:
            produtos.append(produto)
        if input("Deseja cadastrar mais algum produto? (S/N)").upper() != 'S':
            break
    return produtos

def atualizar(produto = None):
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
        produto = escolherProduto(produtos)
        if not produto:
            return
        vendedor = buscarPorId("Vendedores", produto.get("id_vendedor"))
        if not vendedor:
            return
        elif not vendedor.get("produtos"):
            print("Este produto foi vendido, não podendo ser alterado!")
            return
        
        vendido = True
        for id_produto in vendedor.get("produtos"):
            if id_produto == produto.get("id"):
                vendido = False
                break

        if vendido:
            print("Este produto foi vendido, não podendo ser alterado!")
            return

    while True:
        print(separador1)
        print("Produto atual:")
        visualizarProduto(produto, True)
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja alterar?")
        print(separador2)
        print("1 - Nome")
        print("2 - Preço")
        print(separador2)
        print("0 - Salvar e sair")
        print(f'{separador1}\n')

        print("Qual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        limparTerminal()
        if opcaoEscolhida == '0':
            atualizar = atualizarDado("Produtos", produto)
            if not atualizar:
                return
            print("Produto atualizado com sucesso!")
            return
        elif opcaoEscolhida == '1':
            produto["nome_produto"] = entrada("Insira o novo nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        elif opcaoEscolhida == '2':
            produto["valor_produto"] = float(entrada("Insira o novo valor do produto", "Float", "Valor Inválido. Deve conter apenas o número decimal."))
        else:
            print("Insira uma opção válida.")

def deletar(produto = None):
    comVendedor = True if produto == None else False
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
        produto = escolherProduto(produtos)
        if not produto:
            return None
        vendedor = buscarPorId("Vendedores", produto.get("id_vendedor"))
        if not vendedor:
            return None
        elif not vendedor.get("produtos"):
            print("Este produto foi vendido, não podendo ser deletado!")
            return None

        vendido = True
        for produto_a_venda in vendedor["produtos"]:
            if produto_a_venda == produto.get("id"):
                vendido = False
                break

        if vendido:
            print("Este produto foi vendido, não podendo ser deletado!")
            return None

    visualizarProduto(produto, True, comVendedor)
    if entrada("Deseja realmente deletar este produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        if comVendedor:
            vendedor["produtos"].remove(produto.get("id"))
            atualizar = atualizarDado("Vendedores", vendedor)
            if not atualizar:
                return None
            print("Produto removido do vendedor!")

        excluir = excluirProduto("Produtos", produto.get("id"))
        if not excluir:
            return None
        print("Produto deletado com sucesso!")
    return produto.get("id")

def listar():
    produtos = []
    if entrada("Deseja procurar um produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
    else:
        produtos = buscarTodos("Produtos")

    if not produtos:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 0:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 1:
        print(separador1)
        visualizarProduto(produtos[0], comVendedor = True)
        print(separador1)
    else:
        for numeroProduto, produto in enumerate(produtos, start = 1):
            print(separador1)
            print(f'{numeroProduto}º produto:')
            visualizarProduto(produto, comVendedor = True)
        print(separador1)

def gerenciar(vendedor):
    if not vendedor:
        return
    produtos = []
    if vendedor.get("produtos"):
        produtos = vendedor["produtos"]
    while True:
        quantidade = len(produtos)

        print(separador1)
        print("Produtos atuais:")
        if quantidade > 0:
            for produto_id in produtos:
                produto = buscarPorId("Produtos", produto_id)
                print(separador2)
                if produto:
                    visualizarProduto(produto)
                else:
                    print(f"Id inválido para produto: {produto_id}")
            print(separador2)
        else:
            print("Produto: Nenhum produto encontrado")
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar um produto")
        if quantidade > 0:
            print("2 - Atualizar um produto")
            print("3 - Deletar um produto")
        print(separador2)
        print("0 - Salvar e sair")
        print(separador1)
        
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        if opcaoEscolhida == "0":
            break
        elif opcaoEscolhida == "1":
            produto = cadastrar(vendedor)
            if produto:
                produtos.append(produto)
        elif opcaoEscolhida == "2" and quantidade > 0:
            produto = escolherProduto(produtos)
            if produto:
                atualizar(produto)
        elif opcaoEscolhida == "3" and quantidade > 0:
            produto = escolherProduto(produtos)
            if not produto:
                continue
            deletou = deletar(produto)
            if deletou:
                produtos.remove(produto.get("id"))
        else:
            print("Insira uma opção válida.")
    return produtos