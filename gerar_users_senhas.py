import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Marden', 'Gustavo', 'Elvis', 'Morato', 'Admin']
usernames = ['marden', 'gustavo', 'elvis', 'morato', 'admin']
passwords = ['12345abc', '12345abc', '12345abc', 'loja123456', 'Admin@*2022']
# depois de criar o arquivo voltar aqui para ocultar a senha. Pode colocar XXX em cada uma delas

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)

