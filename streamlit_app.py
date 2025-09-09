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

        st.stop()

    # Página estilo ChatGPT (executa somente após login bem-sucedido)
    # Inicialização do estado
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Você é um assistente útil e objetivo."}
        ]

    # Sidebar
    with st.sidebar:
        st.markdown(f"**Usuário:** {st.session_state.usuario}")
        if st.button("Nova conversa", use_container_width=True):
            st.session_state.messages = st.session_state.messages[:1]
            st.rerun()
        if st.button("Sair", type="secondary", use_container_width=True):
            del st.session_state.usuario
            st.rerun()

    # Estilos leves inspirados no ChatGPT
    st.markdown("""
    <style>
    .chat-container {max-width: 900px; margin: 0 auto;}
    .chat-message {padding: 12px 16px; border-radius: 10px; margin-bottom: 8px; line-height: 1.4;}
    .chat-user {background: #0d6efd22; border: 1px solid #0d6efd44;}
    .chat-assistant {background: #343541; color: #fff;}
    .chat-role {font-size: 11px; text-transform: uppercase; opacity: .6; margin-bottom: 4px;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    st.title("Assistente")

    # Render histórico (pulando a primeira system)
    for msg in st.session_state.messages[1:]:
        role = "Você" if msg["role"] == "user" else "Assistente"
        klass = "chat-user" if msg["role"] == "user" else "chat-assistant"
        st.markdown(
            f"<div class='chat-message {klass}'><div class='chat-role'>{role}</div>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    # Entrada do usuário
    if prompt := st.chat_input("Digite sua pergunta..."):
        # Armazena e mostra imediatamente
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Gera resposta se último for user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Pensando..."):
            try:
                client = OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=700,
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = f"Erro ao gerar resposta: {e}"

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)