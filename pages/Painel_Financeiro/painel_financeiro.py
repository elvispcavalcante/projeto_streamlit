import streamlit as st
from Controllers.ColetarInformacoesApi import coletarInformacoesVendas
import pandas as pd
import numpy as np
import datetime
import locale


def painel_financeiro():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')
    st.title("Painel Financeiro")

    with st.form(key='painel_financeiro', clear_on_submit=True):
        input_data_coleta = st.date_input(label='Digite a uma data')
        input_data_coleta = input_data_coleta.strftime('%d/%m/%Y')
        botao_coletar_info = st.form_submit_button(label="Buscar na API as informações de venda")

    if botao_coletar_info:
        df = coletarInformacoesVendas(input_data_coleta)

        df_selecao = df[['data_venda', 'valor_total_venda', 'nome_entregador', 'cpf', 'nome_cliente', 'Endereço',
                         'distancia', 'valor_por_km', 'valor_a_pagar']]
        df_selecao.rename(columns={'data_venda': 'DATA DA VENDA',
                                   'valor_total_venda': 'VALOR TOTAL DA VENDA',
                                   'nome_entregador': 'ENTREGADOR', 'cpf': 'CPF DO ENTREGADOR',
                                   'nome_cliente': 'CLIENTE', 'distancia': 'DISTÂNCIA PERCORRIDA',
                                   'Endereço': 'ENDEREÇO', 'valor_por_km': 'VALOR DO KM',
                                   'valor_a_pagar': 'VALOR A PAGAR AO ENTREGADOR'}, inplace = True)

        pd.set_option('float_format', '{:.2f}'.format)
        pd.set_option('display.precision', 2)
        st.title(f"Vendas efetuadas no dia - {input_data_coleta}")
        st.dataframe(data=df_selecao)

        st.title(f"Valor a pagar aos Entregadores - {input_data_coleta}")
        resultado = df_selecao.groupby(['DATA DA VENDA', 'ENTREGADOR'])['VALOR A PAGAR AO ENTREGADOR'].sum()
        st.dataframe(data=resultado)
