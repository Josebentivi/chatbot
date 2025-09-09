import streamlit as st
import hashlib

 
def hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

if "users" not in st.session_state:
    # Usuários iniciais (senha: 1234)
    st.session_state.users = {"admin": hash_pwd("1234")}

if "modo_registro" not in st.session_state:
    st.session_state.modo_registro = False

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Registrar" if not st.session_state.modo_registro else "Já tenho conta"):
        st.session_state.modo_registro = not st.session_state.modo_registro
        st.rerun()

if st.session_state.modo_registro:
    st.subheader("Criar nova conta")
    with st.form("form_registro"):
        novo_user = st.text_input("Novo usuário")
        nova_senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")
        reg_ok = st.form_submit_button("Registrar")
    if reg_ok:
        if not novo_user or not nova_senha:
            st.error("Preencha todos os campos.")
        elif novo_user in st.session_state.users:
            st.error("Usuário já existe.")
        elif nova_senha != confirmar:
            st.error("Senhas não conferem.")
        else:
            st.session_state.users[novo_user] = hash_pwd(nova_senha)
            st.success("Conta criada. Faça login.")
            st.session_state.modo_registro = False
            time.sleep(1)
            st.rerun()
else:
    st.subheader("Login")
    with st.form("form_login"):
        user = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")
    if entrar:
        if user in st.session_state.users and st.session_state.users[user] == hash_pwd(pwd):
            st.session_state.usuario = user
            st.success("Login realizado.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Credenciais inválidas.")

st.stop()