import pyodbc


class Conexao:

    def criarConexaoDBSQLite(self):
        try:
            # Caso digite errado o nome do arquivo do banco de dados irá ser criado um novo banco
            dados_conexao = "Driver={SQLite3 ODBC Driver};Server=localhost;Database=clickmotobd.db"

            # Se precisar passar um login e senha
            # dados_conexao = "Driver={%s};Server=%s;Database=%s;UID=%s;PWD=%s;"

            conexao = pyodbc.connect(dados_conexao)
            print("Conexão bem sucedida")
        except pyodbc.Error as erro:
            return f'Erro: Não foi possível realizar a conexão com o banco de dados\n"{erro.args[1]}"'

        return conexao

    def fecharConexaoDBSQLite(self, conexao):
        conexao.close()

    def executar_consulta_alteracao(self, conexao: object, query: str):
        cursor = conexao.cursor()
        try:
            cursor.execute(query)
            cursor.commit()
            return 'A consulta foi realizada sucesso!'
        except pyodbc.Error as erro:
            return f'Erro: {erro.args[1]}'

    def executar_consulta_selecao(self, conexao: object, query: str):
        cursor = conexao.cursor()
        try:
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
        except pyodbc.Error as erro:
            return f'Erro: {erro.args[1]}'
