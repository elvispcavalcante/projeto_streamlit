from services.conexao_bd import Conexao
from models.entregadores import Entregador


class EntregadorController:

    # Criando a função para inserir um Entregador
    def inserirEntregador(input_nome_entregador, input_cpf_entregador, input_celular, input_email,
                                          input_agencia, input_tipo_conta, input_num_conta, input_chave_pix):

        entregador_cadastrar = Entregador(input_nome_entregador, input_cpf_entregador, input_celular, input_email,
                                              input_agencia, input_tipo_conta, input_num_conta, input_chave_pix)

        query = "INSERT INTO entregador (nome_entregador, cpf_entregador, celular, email, agencia, tipo_conta, " \
                "num_conta, chave_pix) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (entregador_cadastrar.nome, entregador_cadastrar.cpf, entregador_cadastrar.celular,
                 entregador_cadastrar.email, entregador_cadastrar.agencia, entregador_cadastrar.tipo_conta,
                 entregador_cadastrar.num_conta, entregador_cadastrar.chave_pix)

        conexao = Conexao().criarConexaoDBSQLite()
        resultado = Conexao().executar_consulta_alteracao(conexao, query)
        return resultado
