import streamlit as st
import streamlit_authenticator as stb
from Controllers.EntregadorController import EntregadorController


def entregadores():
    with st.sidebar:
        st.title("Menu")
        # Menu
        st.selectbox(label="", options=['Incluir', 'Consultar'])
    st.header("Cadastro de Clientes")
    with st.form(key='entregadores', clear_on_submit=True):
        tipo_conta = ['Corrente', 'Poupança']
        input_codigo = st.text_input(label='Código', disabled=True)
        input_nome_entregador = st.text_input(label='Nome do entregador', placeholder="Digite o nome completo",
                                              max_chars=70)
        input_cpf_entregador = st.text_input(label="CPF", max_chars=11, placeholder="Digite o CPF somente com os "
                                                                                    "números, sem ponto ou traços")
        input_celular = st.text_input(label='Celular', placeholder='Digite o celular sem parenteses, espaços ou traços',
                                      max_chars=11)
        input_email = st.text_input(label="E-mail", placeholder='Digite o e-mail', max_chars=70)
        input_agencia = st.text_input(label='Agência bancária', placeholder="Digite a agência bancária", max_chars=10)
        input_tipo_conta = st.selectbox(label='Tipo da conta', options=tipo_conta)
        input_num_conta = st.text_input(label='Número da conta', placeholder='Digite o número da conta', max_chars=15)
        input_chave_pix = st.text_input(label='Chave PIX', placeholder='Digite a chave a pix', max_chars=70)

        input_botao_submit = st.form_submit_button('Enviar')

    if input_botao_submit:
        resultado = EntregadorController.inserirEntregador(input_nome_entregador, input_cpf_entregador, input_celular,
                                                           input_email, input_agencia, input_tipo_conta,
                                                           input_num_conta, input_chave_pix)
        print(resultado)
