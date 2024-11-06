from datetime import datetime

from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import usuario as escolherCliente, endereco as escolherEndereco, vendedor as escolherVendedor, produto as escolherProduto, compra as escolherCompra
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1
from Programa.funcoes.utils.visualizar import compra as visualizarCompra

from Programa.funcoes.crud import buscarPorAtributo, buscarPorId, buscarTodos, cadastrar as cadastrarCompra, atualizar as atualizarDado, excluir as excluirCompra


def cadastrar(cliente = None):
    comCliente = False if cliente == None else True
    if not comCliente:
        nome_cliente = entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario.")
        clientes = buscarPorAtributo("Usuarios", "nome_usuario", nome_cliente)
        cliente = escolherCliente(clientes)
        if not cliente:
            return None

    endereco_cliente = escolherEndereco(cliente.get("enderecos"))
    if not endereco_cliente:
        return None

    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
    vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)

    vendedor = escolherVendedor(vendedores)
    if not vendedor:
        return None

    endereco_vendedor = escolherEndereco(vendedor.get("enderecos"))
    if not endereco_vendedor:
        return None
    
    produtos_disponiveis = vendedor["produtos"]
    if not produtos_disponiveis:
        return None

    produtos = set()
    valor_total = 0.0
    while len(produtos_disponiveis) > 0:
        produto = escolherProduto(produtos_disponiveis)
        if not produto:
            return None
        
        produtos_disponiveis.remove(produto.get("id"))
        produtos.add(produto.get("id"))

        valor_total += float(produto.get("valor_produto"))
        if len(produtos_disponiveis) == 0:
            break
        elif entrada("Deseja comprar mais algum produto? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() != 'S':
            break

    if not produtos:
        return None

    compra_realizada={
        "data_compra": datetime.now().replace(microsecond=0),
        "id_cliente": cliente.get("id"),
        "remetente": endereco_vendedor.get("id"),
        "destinatario": endereco_cliente.get("id"),
        "id_vendedor": vendedor.get("id"),
        "produtos": produtos,
        "valor_total": valor_total,
    }
    
    id = cadastrarCompra("Compras", compra_realizada)
    
    if id:
        print("Compra cadastrada com sucesso")
        vendedor["vendas"].add(id)
        vendedor["produtos"] = produtos_disponiveis
        atualizar = atualizarDado("Vendedores", vendedor)
        if not atualizar:
            return None
        print("Vendedor vinculado com sucesso!")

        if not comCliente:
            cliente["compras"].add(id)
            atualizar = atualizarDado("Usuarios", cliente)
            if not atualizar:
                return None
            print("Cliente vinculado com sucesso!")
        return id

def cadastrarMultiplos(cliente):
    compras = cliente.get("compras")
    while True:
        limparTerminal()
        compra = cadastrar(cliente)
        if compra:
            compras.add(compra)
        if entrada("Deseja cadastrar mais alguma compra? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() != 'S':
            break
    return compras

def deletar(vendedor = None):
    comVendedor = False if vendedor == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherVendedor(vendedores)
        if not vendedor:
            return None

    if not vendedor.get("vendas"):
        print("Este vendedor não possui vendas")
        return None
    venda = escolherCompra(vendedor.get("vendas"))
    if not venda:
        return None

    visualizarCompra(venda, True, False, True)
    
    if entrada("Deseja realmente deletar esta venda específica? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        compra_realizada = buscarPorId("Compras", venda.get("id"))

        cliente = buscarPorId("Usuarios", compra_realizada.get("id_cliente"))
        if cliente:
            cliente["compras"].remove(venda.get("id"))
            atualizar = atualizarDado("Usuarios", cliente)
            if not atualizar:
                return None
            print("Compra removida do cliente!")

        for produto in venda["produtos"]:
            vendedor["produtos"].add(produto)

        vendedor["vendas"].remove(venda.get("id"))
        if not comVendedor:
            atualizar = atualizarDado("Vendedores", vendedor)
            if not atualizar:
                return None
        print("Produtos e compras corrigidas com sucesso!")

        excluir = excluirCompra("Compras", venda.get("id"))
        if not excluir:
            return None
        print("Compra deletada com sucesso!")

    return vendedor

def listarCompras():
    compras = []
    if entrada("Deseja procurar as compras de um vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherCliente(vendedores)
        if not vendedor:
            return
        if not vendedor.get("vendas"):
            return
        for id_venda in vendedor.get("vendas"):
            venda = buscarPorId("Compras", id_venda)
            if venda:        
                compras.append(venda)
    else:
        compras = buscarTodos("Compras")

    limparTerminal()
    if not compras:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 0:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 1:
        print(separador1)        
        visualizarCompra(compras[0], comUsuario = True)
        print(separador1)
    else:
        for numeroCompra, compra in enumerate(compras, start = 1):
            print(separador1)
            print(f'{numeroCompra}ª compra:')
            visualizarCompra(compra, comUsuario = True)
        print(separador1)


def listarVendas():
    vendas = []
    if entrada("Deseja procurar as vendas de um usuário específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        usuarios = buscarPorAtributo("Usuarios", "nome_usuario", entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario"))
        cliente = escolherCliente(usuarios)
        if not cliente:
            return
        if not cliente.get("compras"):
            return
        for id_compra in cliente.get("compras"):
            compra = buscarPorId("Compras", id_compra)
            if compra:        
                vendas.append(compra)
    else:
        vendas = buscarTodos("Compras")

    limparTerminal()
    if not vendas:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 0:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 1:
        print(separador1)        
        visualizarCompra(vendas[0], comVendedor = True)
        print(separador1)
    else:
        for numeroVenda, venda in enumerate(vendas, start = 1):
            print(separador1)
            print(f'{numeroVenda}ª venda:')
            visualizarCompra(venda, comVendedor = True)
        print(separador1)