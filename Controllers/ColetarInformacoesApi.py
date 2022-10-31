import requests
from models.venda import Venda
# import pprint
import pandas as pd
import googlemaps
from datetime import datetime, timedelta


def coletarInformacoesVendas(data_vendas_filtrar: str):
    # link da API da COLIBRI para verificar os dados
    link = 'http://localhost:8000/vendas'

    # fazendo a requisão get pelo link acima
    requisicao = requests.get(link)

    # salvando os dados json na variável response
    response = requisicao.json()

    # imprimindo os a response de uma maneira mais legível
    # pprint.pprint(response)

    # criando um dicionário vazio
    vendas = {}

    # preenchendo o dicionário vendas
    for i in range(1, len(response) + 1):
        venda = Venda(data_venda=response[f'{i}']['data_venda'],
                      valor_total_venda=response[f'{i}']['valor_total_venda'],
                      logradouro=response[f'{i}']['endereco']['logradouro'],
                      numero=response[f'{i}']['endereco']['numero'],
                      complemento=response[f'{i}']['endereco']['complemento'],
                      bairro=response[f'{i}']['endereco']['bairro'],
                      municipio=response[f'{i}']['endereco']['municipio'], latitude=response[f'{i}']['latitude'],
                      longitude=response[f'{i}']['longitude'], nome_entregador=response[f'{i}']['nome_entregador'],
                      cpf=response[f'{i}']['cpf'], id_entregador=response[f'{i}']['id_entregador'],
                      id_loja=response[f'{i}']['id_loja'], nome_cliente=response[f'{i}']['nome_cliente'],
                      id_cliente=response[f'{i}']['id_cliente'])

        vendas[i] = {"data_venda": venda.data_venda, "valor_total_venda": venda.valor_total_venda,
                     "logradouro": venda.logradouro, "numero": venda.numero, "complemento": venda.complemento,
                     "bairro": venda.bairro, "municipio": venda.municipio, "latitude": venda.latitude,
                     "longitude": venda.longitude, "nome_entregador": venda.nome_entregador,
                     "cpf": venda.cpf, "id_entregador": venda.id_entregador,
                     "id_loja": venda.id_loja, "nome_cliente": venda.nome_cliente, "id_cliente": venda.id_cliente}

    # criando o DataFrame dos valores do dicionário
    df = pd.DataFrame(data=vendas.values())

    # acrescentando uma coluna Endereço ao DataFrame concatenando os valores das outras colunas
    df['Endereço'] = df["logradouro"].map(str) + ', ' + df["numero"].map(str) + ', ' + df["bairro"].map(str) + \
        ', ' + df["municipio"]
    # Usando a Chave de API do Google Cloud fornecida na ativação ou em credenciais depois de ativada
    gmaps = googlemaps.Client(key='AIzaSyCQXxZQHbwBKcq2rxTNfAvgnAAivUUDXZ4')

    # pegando o endereço da loja e convertando num dicionário geocode
    endereco_loja = gmaps.geocode('Rua Joaquim Marques, 140, Fortaleza')
    # imprimindo o resultado do geocode do endereço da loja
    # pprint.pprint(endereco_loja)

    # formatando o endereço completo de acordo com o google
    enderecos = []
    for index, col in df.iterrows():
        # print(df['Endereço'][index])
        endereco = df['Endereço'][index]
        endereco_google = gmaps.geocode(endereco)
        enderecos.append(endereco_google)

    # inserindo no dataframe a coluna nova. Nesse contexto estou colocando o dicionário completo. No dicionário também
    # tem a localização (location: latitude e longitude)
    df.insert(16, 'dicionario_google_endereco', enderecos, True)

    # ---- Fazendo o cálculo da distância ----
    # lista vazia das distâncias
    distancias = []
    # iterando o dataframe da coluna dicionario_google_endereco e calculando a distância entre o endereço da loja e o
    # endereço do registro da coluna
    for index, col in df.iterrows():
        # pegando o endereço da linha
        endereco_google = df['dicionario_google_endereco'][index]
        # calculando a distância. O retorno é um dicionário
        distancia = gmaps.distance_matrix(origins=endereco_loja[0]['formatted_address'],
                                          destinations=endereco_google[0]['formatted_address'],
                                          departure_time=datetime.now() + timedelta(minutes=5))
        # pegando o valor do dicionário que apresenta a distância em texto
        distancia_formatada = str(distancia['rows'][0]['elements'][0]['distance']['text'])
        # como o retorno é, por exemplo, 3.1 km então separo pelo caractere de espaço para obter uma lista
        separando_distancia = distancia_formatada.split(" ")
        # pego o primeiro valor da lista que é o valor da distância em float
        valor_distancia = float(separando_distancia[0])
        # acrescento a lista de distâncias a distância dos endereços
        distancias.append(valor_distancia)
    # ---- Fim do cálculo da distância ----

    # inserindo a coluna distância no DataFrame
    df.insert(17, 'distancia', distancias, True)

    # valor por Km fornecido pela Loja
    df['valor_por_km'] = 2.30
    # fazendo o cálculo do valor a pagar por venda
    df['valor_a_pagar'] = df['distancia'].map(float) * df['valor_por_km'].map(float)

    # Convertendo a coluna data_venda para o tipo datetime
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    # Criando uma lista de datas formatadas
    datas_formatadas = []
    # Formatando as datas para o formato brasileiro
    for index, col in df.iterrows():
        data_venda = df['data_venda'][index]
        data_venda_brasil = data_venda.strftime('%d/%m/%Y')
        datas_formatadas.append(data_venda_brasil)

    df['data_venda'] = datas_formatadas

    df_data_venda_selecionado = df.loc[df['data_venda'] == data_vendas_filtrar]
    # salvando os dados em uma planilha para ser enviado
    df_data_venda_selecionado.to_excel('teste_dados_mapa.xlsx')

    # calculando por dia o valor total de cada entregador
    resultado = df_data_venda_selecionado.groupby(['data_venda', 'nome_entregador'])['valor_a_pagar'].sum()
    # salvando os dados em uma planilha
    resultado.to_excel('Valor a pagar por entregador.xlsx')
    return df_data_venda_selecionado
