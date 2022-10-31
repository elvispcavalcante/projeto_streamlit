import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import FastMarkerCluster
import googlemaps
import pandas as pd
import fontawesome as fa


def gerarMapa():
    st.title('Mapa de Vendas')
    # Usando a Chave de API do Google Cloud fornecida na ativação ou em credenciais depois de ativada
    gmaps = googlemaps.Client(key='AIzaSyCQXxZQHbwBKcq2rxTNfAvgnAAivUUDXZ4')
    # Lendo como exemplo os pontos do arquivo excel gerado do dia escolhido
    df = pd.read_excel('teste_dados_mapa.xlsx')
    # Pegando as coordenadas no arquivo e transformando numa lista
    locais = df[['latitude', 'longitude']].values.tolist()

    # pegando o endereço da loja e convertando num dicionário geocode
    endereco_loja = gmaps.geocode('Rua Joaquim Marques, 140, Fortaleza')
    # Pegando o endereço, latitude e longitude da loja
    endereco_loja_google = endereco_loja[0]['formatted_address']
    latitude_loja = endereco_loja[0]["geometry"]["location"]["lat"]
    longitude_loja = endereco_loja[0]["geometry"]["location"]["lng"]

    # Criando o mapa
    mapa = folium.Map(location=[latitude_loja, longitude_loja], zoom_start=16)
    folium.Marker(location=[latitude_loja, longitude_loja], popup='Hamburgueria Morato',
                  tooltip="Hamburgueria Morato", icon=folium.DivIcon(html=f"""
    <svg xmlns="http://www.w3.org/2000/svg" fill='red' width='35' height='35' viewBox="0 0 640 512">
    <!--! Font Awesome Pro 6.2.0 by @fontawesome - 
    https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, 
    Inc. --><path d="M36.8 192H603.2c20.3 0 36.8-16.5 36.8-36.8c0-7.3-2.2-14.4-6.2-20.4L558.2 21.4C549.3 8 534.4 0 
    518.3 0H121.7c-16 0-31 8-39.9 21.4L6.2 134.7c-4 6.1-6.2 13.2-6.2 20.4C0 175.5 16.5 192 36.8 192zM64 224V384v80c0 
    26.5 21.5 48 48 48H336c26.5 0 48-21.5 48-48V384 224H320V384H128V224H64zm448 0V480c0 17.7 14.3 32 32 32s32-14.3 
    32-32V224H512z"/></svg>
    """)).add_to(mapa)

    # Adicionando os pontos das vendas no mapa. Dessa forma a cada zoom que for
    FastMarkerCluster(data=locais).add_to(mapa)

    st_data = st_folium(mapa, width=1050, height=500)


