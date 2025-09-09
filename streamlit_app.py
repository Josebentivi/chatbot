import streamlit as st
from openai import OpenAI
import requests
import warnings
from PIL import Image
import time
import uuid
from urllib.parse import urlencode
import hashlib
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

if "usuario" not in st.session_state:

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
else:
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

        
        # Parâmetros do modelo
        model = st.selectbox("Modelo", [ "gpt-5", "gpt-4o-mini"], index=0)

        st.divider()

        # Gerenciamento de conversas
        if "conversations" not in st.session_state:
            st.session_state.conversations = {}  # id -> {title, messages, created_at}
        if "current_conversation_id" not in st.session_state:
            st.session_state.current_conversation_id = None

        def salvar_conversa_atual():
            cid = st.session_state.current_conversation_id
            if cid and st.session_state.chat_messages:
                conv = st.session_state.conversations.get(cid, {})
                conv["messages"] = st.session_state.chat_messages.copy()
                # Atualiza título se ainda padrão
                if conv.get("title") == "Nova conversa":
                    for m in conv["messages"]:
                        if m["role"] == "user":
                            conv["title"] = (m["content"][:40] + "...") if len(m["content"]) > 43 else m["content"]
                            break
                st.session_state.conversations[cid] = conv

        def nova_conversa():
            salvar_conversa_atual()
            cid = str(uuid.uuid4())
            st.session_state.current_conversation_id = cid
            st.session_state.chat_messages = []
            st.session_state.conversations[cid] = {
                "title": "Nova conversa",
                "messages": [],
                "created_at": time.time()
            }
        
        # Definições básicas
        st.session_state.system_prompt = "Você é um assistente útil."

        # Garante que exista uma conversa inicial
        if st.session_state.current_conversation_id is None:
            nova_conversa()

        # Atualiza título (caso o usuário já tenha digitado algo nesta execução)
        salvar_conversa_atual()

        if st.button("🆕 Nova Conversa", use_container_width=True):
            nova_conversa()
            st.rerun()

        st.divider()
        st.markdown("#### Últimas conversas")

        # Ordena por mais recente
        sorted_convs = sorted(
            st.session_state.conversations.items(),
            key=lambda kv: kv[1]["created_at"],
            reverse=True
        )

        for cid, data in sorted_convs:
            selected = (cid == st.session_state.current_conversation_id)
            label = ("➡️ " if selected else "• ") + (data["title"] or "Sem título")
            if st.button(label, key=f"conv_{cid}", use_container_width=True):
                if cid != st.session_state.current_conversation_id:
                    salvar_conversa_atual()
                    st.session_state.current_conversation_id = cid
                    st.session_state.chat_messages = data["messages"].copy()
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