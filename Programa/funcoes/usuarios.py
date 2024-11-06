from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.escolher import usuario as escolherUsuario
from Programa.funcoes.utils.visualizar import usuario as visualizarUsuario

from Programa.funcoes.crud import cadastrar as cadastrarUsuario, atualizar as atualizarUsuario, buscarPorAtributo, buscarTodos, excluir as excluirDado

from Programa.funcoes.enderecos import cadastrarMultiplos as cadastrarEnderecos, gerenciar as gerenciarEnderecos
from Programa.funcoes.favoritos import gerenciar as gerenciarFavoritos
from Programa.funcoes.compras import cadastrarMultiplos as cadastrarCompras

def cadastrar():
    nome = entrada("Insira o nome do usuário", "NaoVazio", "Nome não pode estar em branco.")
    cpf = entrada("Insira o CPF do usuário", "Cpf", "CPF inválido. deve conter apenas os 11 números.")
    email = entrada("Insira o email do usuário", "Email", "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = entrada("Insira o telefone do usuário", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
    
    usuario = {
        "nome_usuario":nome,
        "cpf": cpf,
        "email_usuario": email,
        "telefone_usuario": telefone
    }

    usuario["id"] = cadastrarUsuario("Usuarios", usuario)

    if usuario:
        print("Usuário cadastrado com sucesso!")
        if entrada("Deseja cadastra seus endereços? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não.").upper() == 'S':
            usuario["enderecos"] = cadastrarEnderecos()
            atualizar_enderecos = atualizarUsuario("Usuarios", usuario)
            if not atualizar_enderecos:
                return
            print("Endereços vinculados com sucesso!")

def atualizar():
    nome_usuario = entrada("Insira o nome do usuário", "NaoVazio", "Nome do usuário não pode estar em branco.")
    usuarios_encontrados = buscarPorAtributo("Usuarios", "nome_usuario", nome_usuario)
    usuario = escolherUsuario(usuarios_encontrados)
    if usuario:
        while True:
            print(separador1)
            print("Usuário atual:")
            visualizarUsuario(usuario, True, True, True)
            print(f'{separador1}\n')

            print(separador1)
            print("O que deseja alterar?")
            print(separador2)
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Telefone")
            print("4 - Email")
            print("5 - Enderecos")
            print("6 - Favoritos")
            print(separador2)
            print("7 - Adicionar compras")
            print("0 - Salvar e sair")
            print(f'{separador1}\n')

            print("Qual ação deseja realizar?")
            opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma das opções!")
            limparTerminal()

            if opcaoEscolhida == '0':
                atualizar = atualizarUsuario("Usuarios", usuario)
                if not atualizar:
                    return
                print("Usuario atualizado com sucesso!")
                break
            elif opcaoEscolhida == '1':
                usuario['nome_usuario'] = entrada("Insira o novo nome do usuário", "NaoVazio", "Nome não pode estar em branco.")
            elif opcaoEscolhida == '2':
                usuario['cpf'] = entrada("Insira o novo CPF do usuário", "Cpf", "CPF inválido. deve conter apenas os 11 números.")
            elif opcaoEscolhida == '3':
                usuario['telefone_usuario'] = entrada("Insira o novo telefone do usuário", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            elif opcaoEscolhida == '4':                                       
                usuario['email_usuario'] = entrada("Insira o novo email do usuário", "Email", "Email inválido. Certifique-se de que contém '@' e '.'.")
            elif opcaoEscolhida == '5':
                usuario['enderecos'] = gerenciarEnderecos(usuario.get('enderecos'))
            elif opcaoEscolhida == '6':
                usuario['favoritos'] = gerenciarFavoritos(usuario.get('favoritos'))
            elif opcaoEscolhida == '7':
                usuario['compras'] = cadastrarCompras(usuario)
            else:
                print("Opção inválida!")

def deletar():
    nome_usuario = entrada("Insira o nome do usuário", "NaoVazio", "Nome do usuário não pode estar em branco.")
    usuarios_encontrados = buscarPorAtributo("Usuarios", "nome_usuario", nome_usuario)
    usuario = escolherUsuario(usuarios_encontrados)
    if usuario:
        visualizarUsuario(usuario, True, True, True)
        if entrada("Deseja realmente deletar este usuário específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não.").upper() == 'S':
            if usuario.get("enderecos"):
                for id_endereco in usuario["enderecos"]:
                    deletar = excluirDado("Enderecos", id_endereco)
                    if not deletar:
                        return None
                print("Enderecos deletados com sucesso!")
            deletar = excluirDado("Usuarios", usuario.get("id"))
            if not deletar:
                return
            print("Usuario deletado com sucesso!")

def listar():
    usuarios = []
    if entrada("Deseja procurar um usuario específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        usuarios = buscarPorAtributo("Usuarios", "nome_usuario", entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario"))
    else:
        usuarios = buscarTodos("Usuarios")

    limparTerminal()
    if not usuarios:
        print("Nenhum usuário encontrado!")
    elif len(usuarios) == 0:
        print("Nenhum usuário encontrado!")
    elif len(usuarios) == 1:
        print(separador1)
        visualizarUsuario(usuarios[0], basico = True)
        print(separador1)
    else:
        for numeroUsuario, usuario in enumerate(usuarios, start = 1):
            print(separador1)
            print(f'{numeroUsuario}º usuário:')
            visualizarUsuario(usuario, basico = True)
        print(separador1)