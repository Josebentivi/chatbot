import streamlit as st
import hashlib

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