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

if not st.user.is_logged_in:
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

if not st.user.is_logged_in:
    col = st.columns([1,1,2,1,1],vertical_alignment="center")
    with col[2]:
        # Estiliza o botão de login para incluir o logo do Google
        st.markdown("""
        <style>
        /* Aplica somente ao primeiro botão nesta coluna central (login) */
        div[data-testid="column"] div.stButton button {
            position: relative;
            padding-left: 46px !important;
            height: 48px;
            font-size: 16px;
            font-weight: 600;
            border: 1px solid #dadce0 !important;
            background: #ffffff !important;
            color: #3c4043 !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        div[data-testid="column"] div.stButton button:hover {
            background: #f8faff !important;
            border-color: #d2e3fc !important;
        }
        div[data-testid="column"] div.stButton button:before {
            content: "";
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            width: 24px;
            height: 24px;
            background-repeat: no-repeat;
            background-size: 24px 24px;
            background-image: url("data:image/svg+xml;utf8,<svg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path fill='%234285F4' d='M23.52 12.272c0-.851-.076-1.667-.218-2.455H12v4.642h6.476a5.54 5.54 0 0 1-2.404 3.637v3.02h3.884c2.272-2.093 3.564-5.176 3.564-8.844Z'/><path fill='%2334A853' d='M12 24c3.24 0 5.956-1.075 7.941-2.884l-3.884-3.02c-1.075.72-2.45 1.147-4.057 1.147-3.118 0-5.756-2.105-6.697-4.935H1.31v3.101A11.997 11.997 0 0 0 12 24Z'/><path fill='%23FBBC05' d='M5.303 14.308A7.196 7.196 0 0 1 4.924 12c0-.8.138-1.576.379-2.308V6.591H1.31A11.997 11.997 0 0 0 0 12c0 1.91.458 3.716 1.31 5.409l3.993-3.101Z'/><path fill='%23EA4335' d='M12 4.75c1.764 0 3.348.607 4.596 1.8l3.447-3.447C17.952 1.23 15.236 0 12 0 7.31 0 3.177 2.69 1.31 6.591l3.993 3.101C6.244 6.855 8.882 4.75 12 4.75Z'/><path fill='none' d='M0 0h24v24H0z'/></svg>");
            border-radius: 2px;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Continue com o Google", width="stretch", use_container_width=True):
            st.login()
            st.rerun()
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

        if st.button("Log out", use_container_width=True):
            st.logout()

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