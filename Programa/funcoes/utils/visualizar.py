from Programa.funcoes.utils.formatar import cep, cnpj, cpf, telefone
from Programa.funcoes.utils.separar import separador2, separador3
from Programa.funcoes.crud import buscarPorId

def usuario(usuario, comId = False, comFavoritos = False, comCompras = False, basico = False):
    if comId:
        print(f"ID: {usuario.get('id')}")

    print(f"Nome: {usuario.get('nome_usuario')}")
    print(f"CPF: {cpf(usuario.get('cpf'))}")

    if not basico:
        print(f"Telefone: {telefone(usuario.get('telefone_usuario'))}")
        print(f"Email: {usuario.get('email_usuario')}")
        quantEnderecos = enderecos(usuario.get('enderecos')) if 'enderecos' in usuario else 0

    if comFavoritos:
        quantFavoritos = produtos(usuario.get('favoritos'), favoritos=True)

    if comCompras:
        quantCompras = compras(usuario.get('compras'))

    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comFavoritos:
        fechaSeparador = quantFavoritos > 0
    if fechaSeparador == False and comCompras:
        fechaSeparador = quantCompras > 0
    if fechaSeparador:
        print(separador2)

def vendedor(vendedor, comId = False, comProdutos = False, comVendas = False, basico = False):
    if comId:
        print(f'ID: {vendedor.get("id")}')

    print(f"Nome: {vendedor.get('nome_vendedor')}")
    print(f"CNPJ: {cnpj(vendedor.get('cnpj'))}")

    if not basico:
        print(f"Telefone: {telefone(vendedor.get('telefone_vendedor'))}")
        print(f"Email: {vendedor.get('email_vendedor')}")
        quantEnderecos = enderecos(vendedor.get('enderecos'))

    if comProdutos:
        quantProdutos = produtos(vendedor.get('produtos'))

    if comVendas:
        quantVendas = compras(vendedor.get('vendas'), vendas = True)
    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comProdutos:
        fechaSeparador = quantProdutos > 0
    if fechaSeparador == False and comVendas:
        fechaSeparador = quantVendas > 0
    if fechaSeparador:
        print(separador2)

def compra(compra, comId = False, comVendedor = False, comUsuario = False):
    if comId:
        print(f'ID: {compra.get("id")}')

    print(f'Data da Compra: {compra.get("data_compra")}')

    if comUsuario:
        print(separador2)
        print("Cliente:")
        cliente_compra = buscarPorId("Usuarios", compra.get('id_cliente'))
        if cliente_compra:
            usuario(cliente_compra, basico=True)
        else:
            print(f"Id inválido para usuário: {compra.get('id_cliente')}")

    print(separador2)
    print("Destinatário:")
    destinatario = buscarPorId("Enderecos", compra.get('destinatario'))
    if destinatario:
        endereco(destinatario)
    else:
        print(f"Id inválido para endereço: {compra.get('destinatario')}")
    
    if comVendedor:
        print(separador2)
        print("Vendedor:")
        vendedor_compra = buscarPorId("Vendedores", compra.get('id_vendedor'))
        if vendedor_compra:
            vendedor(vendedor_compra, basico=True)
        else:
            print(f"Id inválido para vendedor: {compra.get('id_vendedor')}")

    print(separador2)
    print("Remetente:")
    remetente = buscarPorId("Enderecos", compra.get('remetente'))
    if remetente:
        endereco(remetente)
    else:
        print(f"Id inválido para endereço: {compra.get('remetente')}")

    print(separador2)
    produtos(compra.get('produtos'))

    print("Total:", compra.get("valor_total"))

def produto(produto, comId=False, comVendedor=False):    
    if comId:
        print(f'ID: {produto.get("id")}')

    print(f"Produto: {produto.get('nome_produto')}")
    print(f"Valor: R${float(produto.get('valor_produto', 0)):.2f}")

    if comVendedor:
        print(separador2)
        vendedor_produto = buscarPorId("Vendedores", produto.get('id_vendedor'))
        if vendedor_produto:
            vendedor(vendedor_produto, basico=True)
        else:
            print(f"Id inválido para vendedor: {produto.get('id_vendedor')}")
        print(separador2)

def endereco(endereco):
    print(f'{endereco.get("rua")}, {endereco.get("numero")} ({endereco.get("descricao")}) - {endereco.get("bairro")}')
    print(f'CEP: {cep(endereco.get("cep"))}')
    print(f'{endereco.get("cidade")} - {endereco.get("estado")} ({endereco.get("pais")})')

def enderecos(enderecos):
    if enderecos == None:
        print("Endereços: Nenhum endereço encontrado")
        return 0
    quantidade = len(enderecos)
    if quantidade == 0:
        print("Endereços: Nenhum endereço encontrado")
    else:
        print(separador2)
        print(f"Endereço{'s' if quantidade > 1 else ''}:")
        for endereco_id in enderecos:
            endereco_item = buscarPorId("Enderecos", endereco_id)
            if endereco_item:
                print(separador3)
                endereco(endereco_item)
            else:
                print(f"Id inválido para endereço: {endereco_id}")
        print(separador3)
    return quantidade

def produtos(produtos, comId = False, favoritos = False):
    titulo = "Produto" if not favoritos else "Favorito"
    if produtos == None:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
        return 0
    quantidade = len(produtos)
    if quantidade == 0:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
    else:
        print(separador2)
        print(f"{titulo}{'s' if quantidade > 1 else ''}:")
        
        for produto_id in produtos:
            produto_item = buscarPorId("Produtos", produto_id)
            if produto_item:
                print(separador3)
                produto(produto_item, comId)
            else:
                print(f"Id inválido para produtos: {produto_id}")
        print(separador3)
    return quantidade

def compras(compras, vendas = False):
    titulo = "Compra" if not vendas else "Venda"
    if compras == None:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
        return 0
    quantidade = len(compras)
    if quantidade == 0:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
    else:
        print(separador2)
        print(f"{titulo}{'s' if quantidade > 1 else ''}:")
        for compra_id in compras:
            compra_item = buscarPorId("Compras", compra_id)
            if compra_item:
                print(separador3)
                compra(compra_item, False, not vendas, vendas)
            else:
                print(f"Id inválido para compras: {compra_id}")
        print(separador3)
    return quantidade