from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.crud import buscarPorAtributo, buscarPorId
from Programa.funcoes.utils.escolher import produto as escolherFavorito
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.visualizar import produto as visualizarFavorito
from Programa.funcoes.utils.separar import separador1, separador2

def cadastrar(favoritos):
    nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
    produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)

    produtos_possiveis = []
    for produto in produtos:
        if not produto.get("id") in favoritos:
            produtos_possiveis.append(produto)
    favorito = escolherFavorito(produtos_possiveis)
    if favorito:
        print("Produto favoritado com sucesso!")
        return favorito.get("id")
    return None

def gerenciar(favoritos):
    if not favoritos:
        favoritos = set()
    while True:
        quantidade = len(favoritos)

        print(separador1)
        print("Favoritos atuais:")
        if quantidade > 0:
            for favorito_id in favoritos:
                favorito = buscarPorId("Produtos", favorito_id)
                print(separador2)
                if favorito:
                    visualizarFavorito(favorito, comVendedor = True)
                else:
                    print(f"Id inválido para produto: {favorito_id}")
            print(separador2)
        else:
            print("Favorito: Nenhum favorito encontrado")
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar um favorito")
        if quantidade > 0:
            print("2 - Remover um favorito")
        print(separador2)
        print("0 - Salvar e sair")
        print(separador1)
        
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        if opcaoEscolhida == "0":
            return favoritos
        elif opcaoEscolhida == "1":
            favorito = cadastrar(favoritos)
            if favorito:
                favoritos.add(favorito)
        elif opcaoEscolhida == "2":
            favoritoEscolhido = escolherFavorito(favoritos, True)
            if favoritoEscolhido:
                favoritos.remove(favoritoEscolhido.get("id"))
        else:
            print("Insira uma opção válida.")