from json import load
from os.path import exists

from Programa.funcoes.utils.salvarErro import salvarErro

secureConnect = 'Programa/conexaoBanco/secureConnect.zip'
token = 'Programa/conexaoBanco/token.json'

def configuracao():
    try:
        if not exists(secureConnect):
            raise FileNotFoundError(f"Arquivo não encontrado: {secureConnect}")
        if not exists(token):
            raise FileNotFoundError(f"Arquivo não encontrado: {token}")
            
        configNuvem = {'secure_connect_bundle': secureConnect}
        with open(token) as f:
            segredos = load(f)
        idCliente = segredos["clientId"]
        segredoCliente = segredos["secret"]
        return configNuvem, idCliente, segredoCliente
    except FileNotFoundError as e:
        salvarErro("Arquivo de configuração não encontrado", e)
        return None, None, None
    except KeyError as e:
        salvarErro("Chave ausente no arquivo de configuração", e)
        return None, None, None
    except Exception as e:
        salvarErro("Erro ao carregar configurações", e)
        return None, None, None

def tabelas():
    return [
        """
        CREATE TABLE IF NOT EXISTS enderecos (
            id UUID PRIMARY KEY,
            rua TEXT,
            numero TEXT,
            descricao TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            pais TEXT,
            cep TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS compras (
            id UUID PRIMARY KEY,
            data_compra TIMESTAMP,
            id_cliente UUID,
            destinatario UUID,
            id_vendedor UUID,
            remetente UUID,
            produtos SET<UUID>,
            valor_total DECIMAL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id UUID PRIMARY KEY,
            nome_usuario TEXT,
            cpf TEXT,
            email_usuario TEXT,
            telefone_usuario TEXT,
            enderecos SET<UUID>,
            favoritos SET<UUID>,
            compras SET<UUID>
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS vendedores (
            id UUID PRIMARY KEY,
            nome_vendedor TEXT,
            cnpj TEXT,
            email_vendedor TEXT,
            telefone_vendedor TEXT,
            enderecos SET<UUID>,
            produtos SET<UUID>,
            vendas SET<UUID>
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id UUID PRIMARY KEY,
            nome_produto TEXT,
            valor_produto DECIMAL,
            id_vendedor UUID
        );
        """
    ]

def indices():
    return [
        "CREATE INDEX IF NOT EXISTS ON usuarios (nome_usuario);",
        "CREATE INDEX IF NOT EXISTS ON vendedores (nome_vendedor);",
        "CREATE INDEX IF NOT EXISTS ON produtos (nome_produto);"
    ]