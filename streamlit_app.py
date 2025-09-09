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
        
        else:
            st.subheader("Login")
            with st.form("form_login"):
                user = st.text_input("Usuário")
                pwd = st.text_input("Senha", type="password")
                entrar = st.form_submit_button("Entrar", width="stretch")
            if entrar:
                if user in st.session_state.users and st.session_state.users[user] == hash_pwd(pwd):
                    st.session_state.usuario = user
                    st.success("Login realizado.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

        #st.stop()

        # Interface principal (executa após login bem-sucedido)
        st.set_page_config(page_title="O Pensador - Chat", page_icon="🧠", layout="wide")

        # Sidebar: configurações
        with st.sidebar:
            st.markdown("### Configurações")
            if "openai_api_key" not in st.session_state:
                st.session_state.openai_api_key = ""
            if "OPENAI_API_KEY" in st.secrets:
                chave = "OK (st.secrets)"
            else:
                st.session_state.openai_api_key = st.text_input("Chave OpenAI", type="password", value=st.session_state.openai_api_key)
                chave = "Informada" if st.session_state.openai_api_key else "Não definida"

            model = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "o3-mini"], index=0)
            temperature = st.slider("Temperatura", 0.0, 1.5, 0.7, 0.05)
            system_default = "Você é um assistente útil, objetivo e explica claramente."
            if "system_prompt" not in st.session_state:
                st.session_state.system_prompt = system_default
            st.session_state.system_prompt = st.text_area("System Prompt", st.session_state.system_prompt, height=120)
            col_sb1, col_sb2 = st.columns(2)
            with col_sb1:
                if st.button("Limpar Chat"):
                    st.session_state.chat_messages = []
                    st.rerun()
            with col_sb2:
                if st.button("Reset Prompt"):
                    st.session_state.system_prompt = system_default
                    st.rerun()
            st.caption(f"Chave: {chave}")

        # Inicializa histórico
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        # Função de chamada ao modelo
        def gerar_resposta():
            try:
                api_key = st.secrets.get("OPENAI_API_KEY") or st.session_state.openai_api_key
                if not api_key:
                    st.error("Informe a chave da API na barra lateral.")
                    return
                client = OpenAI(api_key=api_key)

                messages = [{"role": "system", "content": st.session_state.system_prompt}]
                messages.extend(st.session_state.chat_messages)

                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature
                )
                resposta = resp.choices[0].message.content.strip()
                st.session_state.chat_messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro: {e}")

        # UI principal do chat
        st.markdown("## 💬 Chat")
        for m in st.session_state.chat_messages:
            with st.chat_message("user" if m["role"] == "user" else "assistant"):
                st.markdown(m["content"])

        prompt = st.chat_input("Digite sua mensagem...")
        if prompt:
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                with st.spinner("Pensando..."):
                    gerar_resposta()
                # Render a última resposta adicionada
                if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "assistant":
                    placeholder.markdown(st.session_state.chat_messages[-1]["content"])