import streamlit as st
from openai import OpenAI
import requests
import warnings
from PIL import Image
import time
import uuid
from urllib.parse import urlencode

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
    # === Google OAuth (Login com Gmail) ===
    # Adicionar em .streamlit/secrets.toml:
    # [google]
    # client_id = "SEU_CLIENT_ID.apps.googleusercontent.com"
    # client_secret = "SEU_CLIENT_SECRET"
    # redirect_uri = "http://localhost:8501"  # ou a URL implantada


    AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
    SCOPE = "openid email profile"

    google_cfg = st.secrets.get("google", {})
    CLIENT_ID = google_cfg.get("client_id", "")
    CLIENT_SECRET = google_cfg.get("client_secret", "")
    REDIRECT_URI = google_cfg.get("redirect_uri", "http://localhost:8501")

    query_params = st.query_params()

    # Logout
    if query_params.get("logout"):
        for k in ("usuario", "google_tokens", "oauth_state"):
            st.session_state.pop(k, None)
        st.query_params()
        st.rerun()

    if "usuario" not in st.session_state:
        # Fluxo de autorização inicial
        if "code" not in query_params:
            state = str(uuid.uuid4())
            st.session_state["oauth_state"] = state
            auth_url = AUTH_ENDPOINT + "?" + urlencode({
                "client_id": CLIENT_ID,
                "response_type": "code",
                "scope": SCOPE,
                "redirect_uri": REDIRECT_URI,
                "state": state,
                "access_type": "offline",
                "prompt": "consent"
            })
            st.markdown(
                f'<div style="text-align:center; margin-top:20px;">'
                f'<a href="{auth_url}"><button style="padding:10px 18px; font-size:16px;">Entrar com Google</button></a>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            # Troca de código por tokens
            if query_params.get("state", [""])[0] != st.session_state.get("oauth_state"):
                st.error("Estado inválido. Recarregue a página.")
            else:
                code = query_params["code"][0]
                data = {
                    "code": code,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
                resp = requests.post(TOKEN_ENDPOINT, data=data)
                if resp.status_code == 200:
                    tokens = resp.json()
                    access_token = tokens.get("access_token")
                    headers = {"Authorization": f"Bearer {access_token}"}
                    userinfo = requests.get(USERINFO_ENDPOINT, headers=headers).json()
                    if userinfo.get("email"):
                        st.session_state["usuario"] = {
                            "nome": userinfo.get("name"),
                            "email": userinfo.get("email"),
                            "foto": userinfo.get("picture")
                        }
                        st.session_state["google_tokens"] = tokens
                        st.query_params()  # limpa ?code=...
                        st.rerun()
                    else:
                        st.error("Não foi possível obter dados do usuário.")
                else:
                    st.error("Falha ao autenticar no Google.")
    else:
        # Usuário autenticado
        u = st.session_state["usuario"]
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            if u.get("foto"):
                st.image(u["foto"], width=96)
            st.success(f"Logado como: {u.get('nome')} ({u.get('email')})")
            if st.button("Sair"):
                st.query_params(logout="1")
                st.rerun()


