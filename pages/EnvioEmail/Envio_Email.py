import streamlit as st
import time
from Controllers.EnvioEmailController import enviarEmail


def envioDeEmail():
    st.title('Envio de E-mail')
    with st.form(key='EnvioDeEmail', clear_on_submit=True):
        input_email = st.text_input(label='E-mail', placeholder='Digite um e-mail válido', max_chars=70)
        botao_enviar_email = st.form_submit_button(label='Enviar E-mail')

    if botao_enviar_email:
        if input_email == '':
            with st.empty():
                for seconds in range(1):
                    st.warning("Por favor digite seu usuário e senha", icon="🚨")
                    time.sleep(2)
                st.write("")
        else:
            enviarEmail(input_email)
            with st.empty():
                for seconds in range(1):
                    st.success("E-mail enviado com sucesso", icon="✅")
                    time.sleep(2)
                st.write("")