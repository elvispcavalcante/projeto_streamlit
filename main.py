import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
from PIL import Image
import base64
import time
import datetime
import locale
from pages.Painel_Financeiro.painel_financeiro import painel_financeiro
from pages.Mapa.mapa import gerarMapa
from pages.EnvioEmail.Envio_Email import envioDeEmail


# definição de configurações da página
st.set_page_config(page_title="Km Gestão", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# lendo as imagens que podemos usar na página
background = Image.open('images/fundo.png')
logo = Image.open('images/logo_empresa.png')
corpo_app = None


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


# --- USER AUTHENTICATION ---
names = ['Marden', 'Gustavo', 'Elvis', 'Morato', 'Admin']
usernames = ['marden', 'gustavo', 'elvis', 'morato', 'admin']

# Abrindo o hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# Convertendo os dados em dicionário
dic = {}
for i in range(len(names)):
    dic[usernames[i]] = {'name': names[i], 'password': hashed_passwords[i]}

dic1 = {'usernames': dic}

# Como será a autenticação e tempo de duração do cookie
authenticator = stauth.Authenticate(credentials=dic1, cookie_name="info_users",
                                    key="ProjetoClikMoto&2022", cookie_expiry_days=30)

# Criação de colunas  para lançar na coluna do meio o formulário
col1, col2, col3 = st.columns(3)

# Criação do formulário
with col2:
    # st.image(image=logo, width=300)
    # Coletando os dados da autenticação
    name, authentication_status, username = authenticator.login(form_name='Login', location='main')

# Mudar o css do Botão e Label
st.markdown('''
<style>
    .stButton > button {
        font-weight: bold;
        width: 100%;
    }
    .stTextInput > label {
        font-size:105%; font-weight:bold;
    } "
</style>
''', unsafe_allow_html=True)

# Alterando os labels do formulário de login
my_js = ("""
<style>
    .element-container{
        display: none;
    }
</style>
<script type="text/javascript">
    window.onload = function(){
        //alert("teste")
        var x = window.parent.document.getElementsByClassName("effi0qh3")[0];
        var y = window.parent.document.getElementsByClassName("effi0qh3")[1];
        x.innerHTML = "Usuário";
        y.innerHTML = "Senha";
    }
</script>
""")
components.html(my_js)

# Testes para carregar a página e erros
if authentication_status is False:
    with st.empty():
        for seconds in range(1):
            st.error('Usuário ou senha inválidos. Tente novamente', icon="🚨")
            time.sleep(2)
        st.write("")

if authentication_status is None:
    with st.empty():
        for seconds in range(1):
            st.warning("Por favor digite seu usuário e senha", icon="🚨")
            time.sleep(2)
        st.write("")

# --- CARREGANDO A TELA PRINCIPAL ---
if authentication_status:
    # --- SIDEBAR ---
    with st.sidebar:
        st.write(f'Seja bem-vindo, **{name}**!')

        locale.setlocale(locale.LC_ALL, 'pt_BR')

        st.write(f'{datetime.date.today().strftime("%d de %B de %Y")}')

        authenticator.logout("Sair do Sistema", "sidebar")

        selected = option_menu(
            menu_title='Menu Principal',
            options=["Home", "Painel Financeiro", 'Enviar E-mail', 'Mapas', 'Alterar Senha']
        )
    # --- FIM DO SIDEBAR ---

    # LIMPAR ESPAÇO DE COMPONENT PARA SUBIR O TEXTO A SER EXIBIDO
    components.html("""
    <script type="text/javascript">
        window.onload = function(){
            //alert("teste")
            var a = window.parent.document.getElementsByClassName('css-gsvzp9 e8zbici2')[0]
            var b = window.parent.document.getElementsByClassName('element-container css-1rtpt1n e1tzin5v3')[1]
            var c = window.parent.document.getElementsByClassName('element-container css-1rtpt1n e1tzin5v3')[2]
            var d = window.parent.document.getElementsByClassName('element-container css-1rtpt1n e1tzin5v3')[3]
            var e = window.parent.document.getElementsByClassName('element-container css-1rtpt1n e1tzin5v3')[4]
            var f = window.parent.document.getElementsByClassName('element-container css-1rtpt1n e1tzin5v3')[5]
            var y = window.parent.document.getElementsByClassName("e1tzin5v3")[9];
            var z = window.parent.document.getElementsByClassName("e1tzin5v3")[10];
            var w = window.parent.document.getElementsByClassName("e1tzin5v3")[11];
            var t = window.parent.document.getElementsByClassName("e1tzin5v3")[12];
            var i = window.parent.document.querySelectorAll('iframe')[4];
            a.setAttribute("style","display: none;");
            b.setAttribute("style","display: none;");
            c.setAttribute("style","display: none;");
            d.setAttribute("style","display: none;");
            e.setAttribute("style","display: none;");
            i.attributes.style.value = 'overflow: hidden; display:none;';
            
        }
    </script>
    """)

    if selected == 'Home':
        st.title(f'Seja bem-vindo, **{name}**! Clique no menu lateral esquerdo para navegar no sistema.')

    if selected == "Painel Financeiro":
        painel_financeiro()

    if selected == 'Enviar E-mail':
        envioDeEmail()

    if selected == 'Mapas':
        gerarMapa()

    if selected == 'Alterar Senha':
        if authentication_status:
            try:
                components.html(
                    """
                    <script type="text/javascript">
                        window.onload = function(){
                            window.parent.document.getElementsByClassName("css-10trblm e16nr0p30")[0].innerHTML = 
                            "Alterar Senha";
                            window.parent.document.getElementsByClassName("css-1o3im13 effi0qh3")[0].innerHTML = 
                            "Senha Atual";
                            window.parent.document.getElementsByClassName("css-1o3im13 effi0qh3")[1].innerHTML = 
                            "Nova Senha";
                            window.parent.document.getElementsByClassName("css-1o3im13 effi0qh3")[2].innerHTML = 
                            "Repita a Nova Senha";
                            window.parent.document.getElementsByClassName("css-1n4ot0l edgvbvh5")[0].innerHTML = 
                            "Atualizar a Senha";
                        }
                    </script>
                    """
                )
                with st.container():
                    if authenticator.reset_password(username, 'Reset password'):
                        st.success('A senha foi modificada com sucesso!')
            except Exception as e:
                st.error(e)
