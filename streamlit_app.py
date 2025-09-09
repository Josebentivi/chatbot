import streamlit as st
from openai import OpenAI
import requests
import warnings
from PIL import Image
import time
import uuid
from urllib.parse import urlencode
import hashlib

if "usuario" not in st.session_state:
    # Suppress Streamlit's ScriptRunContext warning
    warnings.filterwarnings("ignore", message="missing ScriptRunContext")
    st.set_page_config(
        page_title="O Pensador Desktop",
        page_icon=":thought_balloon:",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }) 

    with st.container(height=50,border=False):
        st.empty()
    with st.container(height=100,border=False):
        rainbow_colors = ["#FFB3BA", "#FEDEBA", "#FEFDBB", "#B9FEC9", "#BAE0FF", "#CFD2FF", "violet"]
        #rainbow_colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        text = ["Revolucionando"," a ","Maneira"," de"," Pensar"," e"," Aprender"]
        rainbow_text = ""
        color_index = 0

        for char in text:
            if char != " ":
                color = rainbow_colors[color_index % len(rainbow_colors)]
                rainbow_text += f'<span style="color: {color};">{char}</span>'
                color_index += 1
            else:
                rainbow_text += " "

        st.markdown(
            f'<div style="text-align: center; font-size: 24px; font-weight: bold;">{rainbow_text}</div>',
            unsafe_allow_html=True
        )
    col = st.columns([1,1,1],vertical_alignment="center")
    with col[1]:
        def hash_pwd(pwd: str) -> str:
            return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

        if "users" not in st.session_state:
            # Usuários iniciais (senha: 1234)
            st.session_state.users = {"admin": hash_pwd("1234")}

        if "modo_registro" not in st.session_state:
            st.session_state.modo_registro = False
            # Move the "Registrar"/"Já tenho conta" toggle button next to the "Entrar" submit button using DOM manipulation
            st.markdown("""
            <style>
            /* Make buttons inline when placed together */
            .stButton > button {
                white-space: nowrap;
            }
            </style>
            <script>
            function relocateButtons(){
                const allButtons = Array.from(document.querySelectorAll('button'));
                const registrarBtn = allButtons.find(b => /Registrar|Já tenho conta/.test(b.innerText.trim()));
                const entrarBtn = allButtons.find(b => b.innerText.trim() === 'Entrar');
                if (!registrarBtn || !entrarBtn) return;

                // Avoid re-appending if already adjacent
                if (entrarBtn.nextSibling === registrarBtn) return;

                // Append registrar button right after entrar button
                entrarBtn.parentElement.appendChild(registrarBtn);
                registrarBtn.style.marginLeft = '0.5rem';
            }

            const observer = new MutationObserver(() => relocateButtons());
            observer.observe(document.body, {childList: true, subtree: true});
            window.addEventListener('load', relocateButtons);
            setTimeout(relocateButtons, 500);
            setInterval(relocateButtons, 1500);
            </script>
            """, unsafe_allow_html=True)
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