import streamlit as st
from PIL import Image
import time
import base64


def logar():
    # lendo as imagens que podemos usar na página
    background = Image.open('images/fundo.png')
    logo = Image.open('images/logo_empresa.png')

    # definição de configurações da página
    st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

    # Função para ler a imagem e transformar em base64
    @st.cache(allow_output_mutation=True)
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Função para jogar a imagem como plano de fundo da página
    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: auto;
        background-repeat: no-repeat;
        background-attachment: scroll; # doesn't work
        }
        </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return

    # Chamando a função para colocar o background
    set_png_as_page_bg(r'images/fundo.png')

    # Mudar configurações label
    st.markdown('''
    <style>
    .stTextInput > label { 
        font-size:105%; font-weight:bold;} "
    </style>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <style>
        .stButton > button {
            font-weight: bold;
            width: 100%
        }
    </style>
    ''', unsafe_allow_html=True)

    # Criação de colunas  para lançar na coluna do meio o formulário
    col1, col2, col3 = st.columns(3)

    # Criação do formulário
    with col2:
        st.image(image=logo, width=300)
        with st.form(key='login', clear_on_submit=False):
            input_login = st.text_input(label='Usuário', placeholder='Digite o seu usuário')
            input_password = st.text_input(label='Senha', placeholder='Digite a sua senha', type='password')
            input_entrar = st.form_submit_button('Entrar')

    # Testes após a clicar no botão enviar
    if input_entrar:

        if input_login == '':
            with st.empty():
                for seconds in range(2):
                    st.error("Oops! O login está vazio! Digita o login cara", icon="🚨")
                    time.sleep(1)
                st.write("")
        if input_password == '':
            with st.empty():
                for seconds in range(2):
                    st.error("Ei mano a senha está vazia! Digita a senha", icon="🚨")
                    time.sleep(1)
                st.write("")
        if input_login and input_password:
            st.experimental_set_query_params(page='login')
