from Programa.conexaoBanco.conectar import conectar
from Programa.funcoes.utils.salvarErro import salvarErro
from Programa.funcoes.utils.converter import rowParaDict

from cassandra.query import SimpleStatement
from uuid import uuid4, UUID

sessao = conectar()

def escolherColecao(nome):
    if sessao is None:
        salvarErro("Erro na sessão", "Sessão de banco de dados não estabelecida")
        return None

    colecoes = {
        'Usuarios': 'usuarios',
        'Vendedores': 'vendedores',
        'Produtos': 'produtos',
        'Compras': 'compras',
        'Enderecos': 'enderecos'
    }
    return colecoes.get(nome)

def cadastrar(nomeColecao, dados):
    colecao = escolherColecao(nomeColecao)
    if colecao is None:
        return None
    try:
        colunas = ', '.join(dados.keys())
        valores = []
        
        for v in dados.values():
            if isinstance(v, UUID) or isinstance(v, float) or isinstance(v, int):
                valores.append(f"{v}")
            elif isinstance(v, set):
                set_values = ', '.join([str(uuid) for uuid in v])
                valores.append(f"{{{set_values}}}")
            else:
                valores.append(f"'{v}'")
        
        valores_str = ', '.join(valores)
        id = uuid4()
        query = f"INSERT INTO {colecao} (id, {colunas}) VALUES ({id}, {valores_str})"
        sessao.execute(SimpleStatement(query))
        return id

    except Exception as e:
        salvarErro(f"Erro ao cadastrar em {nomeColecao}", e)
        return None

def atualizar(nomeColecao, dados):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        updates = []
        for k, v in dados.items():
            if k != "id":
                if isinstance(v, set):
                    set_values = ', '.join([str(uuid) for uuid in v])
                    updates.append(f"{k} = {{{set_values}}}")
                elif isinstance(v, (int, float)):
                    updates.append(f"{k} = {v}")
                elif isinstance(v, UUID):
                    updates.append(f"{k} = {str(v)}")
                else:
                    updates.append(f"{k} = '{v}'")
                    
        updates_str = ', '.join(updates)
        query = f"UPDATE {colecao} SET {updates_str} WHERE id = {dados['id']}"
        sessao.execute(SimpleStatement(query))
        return dados["id"]
    except Exception as e:
        salvarErro(f"Erro ao atualizar {nomeColecao}", e)
        return None

def excluir(nomeColecao, id):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        query = f"DELETE FROM {colecao} WHERE id = {id}"
        sessao.execute(SimpleStatement(query))
        return id
    except Exception as e:
        salvarErro(f"Erro ao excluir em {nomeColecao}", e)
        return None

def buscarTodos(nomeColecao):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        query = f"SELECT * FROM {colecao}"
        resultados = sessao.execute(SimpleStatement(query))
        return [rowParaDict(row, colecao) for row in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar todos os registros", e)
    return None

def buscarPorId(nomeColecao, id):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        query = f"SELECT * FROM {colecao} WHERE id = {id}"
        prepared_stmt = SimpleStatement(query)
        resultado = sessao.execute(prepared_stmt).one()
        if resultado:
            return rowParaDict(resultado, colecao)
        else:
            salvarErro("Registro não encontrado", f'ID {id} não encontrado na colecao {nomeColecao}')
            return None
    except Exception as e:
        salvarErro("Erro ao buscar registro por ID", e)
        return None

def buscarPorAtributo(nomeColecao, nomeCampo, atributo):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        query = f"SELECT * FROM {colecao} WHERE {nomeCampo} = '{atributo}'"
        resultados = sessao.execute(SimpleStatement(query))
        return [rowParaDict(row, colecao) for row in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar registro por atributo semelhante", e)
        return None