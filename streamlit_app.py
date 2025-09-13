import threading
from threading import Thread
import streamlit as st
from openai import OpenAI
import requests
import warnings
from PIL import Image
import time
from time import sleep
import uuid
from urllib.parse import urlencode
import hashlib

#Funções
class RetornoThread(Thread):
    # constructor
    def __init__(self,usuario):
        # execute the base constructor
        Thread.__init__(self)
        self.usuario = usuario
        self.mensagens = []

	# function executed in a new thread
    def run(self):
        try:
            #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/retornarconversa/"
            url = "http://52.2.202.37/produto/post/filosofo/retornarconversa/"
            data = {"data":{"usuario": self.usuario},"chave":st.secrets["CHAVE"]}
            
            self.mensagens = requests.post(url, json=data, timeout=20*60).json().get("saida")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao acessar servidor: {e}")
            st.stop()
            self.mensagens = []

def Carregando(aceleracao=0.1):
    porcentagem = 0
    colsCarregando = st.columns(3)
    item = RetornoThread(st.session_state.usuario)
    item.start()
    retorno = ""

    with colsCarregando[1]:
        my_bar = st.progress(porcentagem, text="Iniciando plataforma...")
        tempo=0.5
        
        porcentagem += 25
        my_bar.progress(porcentagem, text="Carregando Filósofos...")
        tempo+=aceleracao
        sleep(tempo)
        
        porcentagem += 25
        my_bar.progress(porcentagem, text="Carregando Artigos científicos...")
        tempo+=aceleracao
        sleep(tempo)
        
        porcentagem += 25
        my_bar.progress(porcentagem, text="Aprimorando inteligência...")
        tempo+=aceleracao
        item.join()
        sleep(tempo)
        
        porcentagem += 25
        my_bar.progress(porcentagem, text="Finalizando...")
        tempo+=aceleracao
        time.sleep(tempo)
        retorno = item.mensagens
        my_bar.empty()
    #st.text(retorno)
    if retorno:
        return retorno
    else:
        return []

    #st.session_state.carregado = True
def desativar_marcacoes():
    if st.session_state.marcar_artigos:
        st.session_state.marcar_artigos = False
    if st.session_state.marcar_pensadores:
        st.session_state.marcar_pensadores = False
    if st.session_state.acessando_livros:
        st.session_state.acessando_livros = False

if "acessando_livros" not in st.session_state:
    st.session_state.acessando_livros = False
if st.session_state.acessando_livros:
    desativar_marcacoes()

def ativar_artigos():
    if st.session_state.marcar_artigos:
        st.session_state.marcar_pensadores = False
        if st.session_state.selected_thinker:
            st.session_state.selected_thinker = None

def ativar_menu():
    if st.session_state.marcar_artigos:
        st.session_state.marcar_pensadores = False
        if st.session_state.selected_thinker:
            st.session_state.selected_thinker = None

def ativar_pensadores():
    if st.session_state.marcar_pensadores:
        st.session_state.marcar_artigos = False
        if st.session_state.selected_thinker is None:
            st.session_state.selected_thinker = "Sigmund Freud"


#st.logout()

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

apresentacao = st.empty()

if not st.user.is_logged_in:
    col = st.columns([1,1,1,1,1],vertical_alignment="center")
    with col[2]:
        google_logo_url = "https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png"
        st.markdown(f"""
        <style>
        .stButton > button {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 0.6rem 1rem;
        }}
        .stButton > button:before {{
            content: "";
            width: 22px;
            height: 22px;
            background-image: url('{google_logo_url}');
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button("Continue com o Google", width="stretch", use_container_width=True):
            st.login()
            st.session_state.apresentacao = True
            st.rerun()
else:
    st.session_state.usuario = str(st.user.sub)
    #st.text(st.user.sub)
    if "messages" not in st.session_state:
        #st.text("Carregando mensagens...")
        if "entrouapresentacao" not in st.session_state:
            textoinicial = """O Pensador é uma ferramenta baseada em inteligência artificial concebida para aprimorar o debate acadêmico e o pensamento crítico. O objetivo central é oferecer um meio pelo qual pesquisadores, estudantes e docentes possam confrontar ideias de forma estruturada, rigorosa e verificável, contrastando argumentos com trechos e referências de obras relevantes e simulando a interação entre diferentes pensadores sobre um mesmo tema.\n\n"""
            with apresentacao.container():
                culunaparesentacao = st.columns([1,2,1],vertical_alignment="center")
                with culunaparesentacao[1]:
                    #st.markdown("### Bem vindo ao Pensador")
                    #st.markdown("#### A revolução do pensamento crítico")
                    #st.markdown("##### Uma ferramenta para debates acadêmicos")
                    #st.markdown("###### Desenvolvido por João Beneti")
                    st.markdown(f"<div style='text-align: center;'>{textoinicial}</div>", unsafe_allow_html=True)
                colsapresentacao = st.columns(5)
                with colsapresentacao[2]:
                    if st.button("Acessar Plataforma", width="stretch", use_container_width=True):
                        st.session_state.entrouapresentacao = True
                        st.rerun()
            st.stop()
        st.session_state.messages = Carregando(aceleracao=0.1)
        apresentacao.empty()
    # Sidebar: configurações
    with st.sidebar:
        #st.markdown("### Configurações")
        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""
        if "OPENAI_API_KEY" in st.secrets:
            chave = "OK (st.secrets)"
        else:
            st.session_state.openai_api_key = st.text_input("Chave OpenAI", type="password", value=st.session_state.openai_api_key)
            chave = "Informada" if st.session_state.openai_api_key else "Não definida"

        
        # Parâmetros do modelo
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "gpt-5-nano"
        #st.session_state.selected_model = "gpt-5-nano"

        if st.session_state.selected_model == "gpt-5-nano":
            st.badge("Plano Gratuito", icon=":material/bolt:", color="red")
            st.badge("IA: Padrão", icon=":material/robot_2:", color="gray")
            st.badge("Pesquisa Literária: Superficial", icon=":material/menu_book:", color="gray")
            st.badge("Mesa de Conversa: 2 Pensadores", icon=":material/person:", color="gray")
            if st.button("Ativar Plano Pro", icon=":material/toggle_off:", use_container_width=True):
                st.session_state.selected_model = "gpt-5"
                st.rerun()
        if st.session_state.selected_model == "gpt-5":
            st.badge("Plano Pro", icon=":material/bolt:", color="green")
            st.badge("IA: Aprimorada", icon=":material/robot_2:", color="orange")
            st.badge("Pesquisa Literária: Profunda", icon=":material/menu_book:", color="orange")
            st.badge("Mesa de Conversa: 4 Pensadores", icon=":material/person:", color="orange")
            if st.button("Ativar Plano Gratuito", icon=":material/toggle_on:", use_container_width=True):
                st.session_state.selected_model = "gpt-5-nano"
                st.rerun()
        st.divider()

        if "selected_thinker" not in st.session_state:
            st.session_state.selected_thinker = None
        #if "selected_model" not in st.session_state or st.session_state.selected_model not in ["gpt-4.1-nano", "gpt-4.1-mini", "o4-mini"]:
        #    #st.session_state.selected_model = "gpt-5"
        #    st.session_state.selected_model = "gpt-5-nano"

        #model_keys = [ "gpt-5", "gpt-5-mini","gpt-5-nano"]
        #model_names = {
        #    "gpt-5": "Gpt-5: Modelo de pensamento para tarefas mais complexas",
        #    "gpt-5-mini": "Gpt-5 Mini: Resposta rápida para tarefas com média complexidade.",
        #    "gpt-5-nano": "Gpt-5 Nano: Resposta rápida para tarefas leves."
        #}
        #selected = st.selectbox(
        #    "Motor do chat:",
        #    options=model_keys,
        #    index=model_keys.index(st.session_state.selected_model),
        #    format_func=lambda key: model_names[key]
        #)
        #st.session_state.selected_model = selected

        # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
        credtstotal,vazio, addcredts = st.columns([0.6,0.2,0.2])
        with credtstotal:
            st.markdown(f"### :green[Creditos: 20]")
        with addcredts:
            if st.button("", icon=":material/add_2:", use_container_width=True):
                pass
        if st.session_state.selected_model == "gpt-5-nano":
            st.text("Chat Padrão (Gratuito)")
            col_checkbox, col_info = st.columns([0.7, 0.3])
            # Cria o checkbox e o ícone de informação na mesma linha
            with col_checkbox:
                marcarArtigos = st.checkbox(
                    "Artigos (Gratuito)", 
                    value=False, 
                    key="marcar_artigos", 
                    on_change=ativar_artigos
                )
            with col_info:
                # Define o texto que aparecerá ao passar o mouse
                info_text = "Com o objetivo de ter um mecanismo de pesquisa imparcial. Desenvolvemos um algoritimo que verifica semânticamente toda nossa base de dados com mais de 220 mil artigos publicados no ano de 2024."
                # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
                st.markdown(
                    f"<span title='{info_text}' style='cursor: pointer;'>&#9432;</span>",
                    unsafe_allow_html=True
                )
            # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
            col_checkbox, col_info = st.columns([0.7, 0.3])
            # Cria o checkbox e o ícone de informação na mesma linha
            with col_checkbox:
                # Cria o checkbox para o modo "Pensadores" e o ícone de informação na mesma linha
                marcarPensador = st.checkbox(
                    "Pensadores (Gratuito)", 
                    value=False, 
                    key="marcar_pensadores", 
                    on_change=ativar_pensadores
                )
            with col_info:
                # Define o texto que aparecerá ao passar o mouse
                info_text = "Tenha uma inteligência artificial treinada nas obras de diversos pensadores. Desbrave o mundo das ideias e encontre respostas para os seus questionamentos mais difíceis."
                # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
                st.markdown(
                    f"<span title='{info_text}' style='cursor: pointer;'>&#9432;</span>",
                    unsafe_allow_html=True
                )
            if st.session_state.marcar_pensadores:
                st.session_state.selected_thinker = st.selectbox(
                    "Selecione o pensador:",
                    options=["Sigmund Freud", "Carl Gustav Jung", "Michel Foucault", "Friedrich Nietzsche","Jiddu Krishnamurti","Santo Agostinho","Santo Tomás de Aquino","Martinho Lutero","Paulo de Tarso"],
                    index=["Sigmund Freud", "Carl Gustav Jung", "Michel Foucault", "Friedrich Nietzsche","Jiddu Krishnamurti","Santo Agostinho","Santo Tomás de Aquino","Martinho Lutero","Paulo de Tarso"].index(st.session_state.selected_thinker)
                )
        elif st.session_state.selected_model == "gpt-5":
            st.text("Chat Pro (1 crédito)")
            col_checkbox, col_info = st.columns([0.7, 0.3])
            # Cria o checkbox e o ícone de informação na mesma linha
            with col_checkbox:
                marcarArtigos = st.checkbox(
                    "Artigos (10 Créditos)", 
                    value=False, 
                    key="marcar_artigos", 
                    on_change=ativar_artigos
                )
            with col_info:
                # Define o texto que aparecerá ao passar o mouse
                info_text = "Com o objetivo de ter um mecanismo de pesquisa imparcial. Desenvolvemos um algoritimo que verifica semânticamente toda nossa base de dados com mais de 220 mil artigos publicados no ano de 2024."
                # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
                st.markdown(
                    f"<span title='{info_text}' style='cursor: pointer;'>&#9432;</span>",
                    unsafe_allow_html=True
                )
            # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
            col_checkbox, col_info = st.columns([0.7, 0.3])
            # Cria o checkbox e o ícone de informação na mesma linha
            with col_checkbox:
                # Cria o checkbox para o modo "Pensadores" e o ícone de informação na mesma linha
                marcarPensador = st.checkbox(
                    "Pensadores (10 Créditos)", 
                    value=False, 
                    key="marcar_pensadores", 
                    on_change=ativar_pensadores
                )
            with col_info:
                # Define o texto que aparecerá ao passar o mouse
                info_text = "Tenha uma inteligência artificial treinada nas obras de diversos pensadores. Desbrave o mundo das ideias e encontre respostas para os seus questionamentos mais difíceis."
                # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
                st.markdown(
                    f"<span title='{info_text}' style='cursor: pointer;'>&#9432;</span>",
                    unsafe_allow_html=True
                )
            if st.session_state.marcar_pensadores:
                st.session_state.selected_thinker = st.selectbox(
                    "Selecione o pensador:",
                    options=["Sigmund Freud", "Carl Gustav Jung", "Michel Foucault", "Friedrich Nietzsche","Jiddu Krishnamurti","Santo Agostinho","Santo Tomás de Aquino","Martinho Lutero","Paulo de Tarso"],
                    index=["Sigmund Freud", "Carl Gustav Jung", "Michel Foucault", "Friedrich Nietzsche","Jiddu Krishnamurti","Santo Agostinho","Santo Tomás de Aquino","Martinho Lutero","Paulo de Tarso"].index(st.session_state.selected_thinker)
                )
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
            #salvar_conversa_atual()
            cid = str(uuid.uuid4())
            st.session_state.current_conversation_id = cid
            #st.session_state.chat_messages = []
            st.session_state.conversations[cid] = {
                "title": "Nova conversa",
                "messages": [],
                "created_at": time.time()
            }
        
        # Atualiza título (caso o usuário já tenha digitado algo nesta execução)
        salvar_conversa_atual()

        #if st.button("Nova Conversa", icon=":material/add:", use_container_width=True):
        #    nova_conversa()
        #    st.rerun()

        if st.button("Limpar Chat", icon=":material/delete:", use_container_width=True):
            try:
                #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/recomecarconversa/"
                url = "http://52.2.202.37/produto/post/filosofo/recomecarconversa/"
                #url = "http://52.2.202.37/produto/post/filosofo/recomecarconversa/"
                data = {"data":{"usuario": st.session_state.usuario},"chave":st.secrets["CHAVE"]}
                requests.post(url, json=data, timeout=5*60).json().get("saida")
                st.session_state.messages = []
                st.rerun(scope="app")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao acessar servidor: {e}")
                st.stop()

        if st.button("Log out", icon=":material/logout:", use_container_width=True):
            st.logout()

        #st.divider()
        #st.markdown("#### Últimas conversas")

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
        
        #st.caption(f"Chave: {chave}")

    x='''
    if not st.session_state.carregado:
        Carregando() 
    else:
        try:
            url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/retornarconversa/"
            #url = "http://52.2.202.37/produto/post/filosofo/retornarconversa/"
            data = {"data":{"usuario": st.session_state.usuario},"chave":st.secrets["CHAVE"]}
            st.session_state.messages = requests.post(url, json=data, timeout=5*60).json().get("saida")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao acessar servidor: {e}")
            st.stop()
    #openai_api_key = st.session_state.openai_api_key'''
    
    
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.

    # Display the existing chat messages via `st.chat_message`.
    if st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown('Olá! Como posso te ajudar?')
        for message in st.session_state.messages:
            if message["role"] == "developer":
                #with st.chat_message("assistant"):
                #    st.markdown(message["content"][0]["text"])
                pass
            elif message["role"] == "ReferenciasArtigos":
                with st.chat_message("assistant"):
                    
                    #st.markdown(message["content"][0]["text"].get("Pesquisa"))
                    for i in ["Pensamento","Análise","Contra-argumentos","Referências da Argumentação","Referências do Contra-argumento"]:
                        with st.status("Acessando Dados.", expanded=False) as status:
                            if i in ["Referências da Argumentação","Referências do Contra-argumento"]:
                                for k in message["content"][0]["text"].get(i).split("+=-!!-=+"):
                                    st.markdown(k)
                            else:
                                st.markdown(message["content"][0]["text"].get(i))

                            status.update(
                                label=f"{i} concluido(a).", state="complete", expanded=False
                            )
            elif message["role"] in ["user", "assistant"]:
                #st.text(message)
                with st.chat_message(message["role"]):
                    st.markdown(message["content"][0].get("text"))

    entradachat = st.empty()
    saidachat = st.empty()
    pensamento1 = st.empty()
    pensamento2 = st.empty()
    pensamento3 = st.empty()
    pensamento4 = st.empty()
    pensamento5 = st.empty()
    pensamento6 = st.empty()
    pensamento7 = st.empty()
    pensamento8 = st.empty()
    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Em que eu posso te ajudar?",accept_file=True,file_type=["jpg", "jpeg", "png","pdf","mp3"],):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": [{"type":"text","text":prompt["text"]}]})
        with entradachat.container():
            with st.chat_message("user"):
                st.markdown(prompt["text"])
        dadosenvio={}
        
        if st.session_state.marcar_artigos == True or st.session_state.marcar_pensadores == True:
            st.session_state.acessando_livros = True
            caminho = ""
            if st.session_state.marcar_artigos == True:
                caminho = "/produto/post/artigos"
            usuario = 0
            with pensamento1.status("Acessando a Biblioteca.", expanded=True) as status:
                if st.session_state.marcar_artigos == True:
                    st.write("Lendo mais de 220 mil Artigos Científicos.")
                else:
                    st.write(f"Lendo todas as obras de {st.session_state.selected_thinker}.")
                with st.spinner("Aguarde. (Tempo de espera médio de 5 minutos)", show_time=True):
                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/artigos/iniciar/"
                        url = f"http://52.2.202.37{caminho}/iniciar/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"stream": 1,
                                "pesquisa": prompt["text"]},
                                "chave":st.secrets["CHAVE"]}
                        if st.session_state.marcar_artigos == False:
                            data["data"]["pensador"] = st.session_state.selected_thinker
                        post_response = requests.post(url, json=data, timeout=20*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao acessar servidor: {e}")
                        st.stop()
                    #st.markdown(post_response.json())
                    usuario = post_response.json().get("saida").get("usuario")
                    client = OpenAI()
                    # Generate a response using the OpenAI API.
                    stream = client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=post_response.json().get("saida").get("mensagem"),
                    stream=True,
                    )
                    spinner = st.empty()
                    response_text = st.write_stream(stream)

                status.update(
                    label="Consulta a biblioteca concluida.", state="complete", expanded=False
                )

            with pensamento2.status("Sabatina", expanded=True) as status:
                st.write("Realizando análise crítica.")
                with st.spinner("Aguarde.", show_time=True):
                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/artigos/continuar/"
                        url = f"http://52.2.202.37{caminho}/continuar/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"stream": 2,
                                "usuario": usuario,
                                "retornostream": response_text},
                                "chave":st.secrets["CHAVE"]}
                        if st.session_state.marcar_artigos == False:
                            data["data"]["pensador"] = st.session_state.selected_thinker
                        post_response = requests.post(url, json=data, timeout=5*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao acessar servidor: {e}")
                        st.stop()
                    #st.markdown(post_response.json())
                    client = OpenAI()
                    # Generate a response using the OpenAI API.
                    stream = client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=post_response.json().get("saida").get("mensagem"),
                    stream=True,
                    )
                    response_text = st.write_stream(stream)

                status.update(
                    label="Sabatina Completa", state="complete", expanded=False
                )
                
            with pensamento3.status("Preparo da Contra-Argumentação", expanded=True) as status:
                st.write("Pesquisando por contra-argumentos.")
                with st.spinner("Aguarde.", show_time=True):
                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/artigos/continuar/"
                        url = f"http://52.2.202.37{caminho}/continuar/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"stream": 3,
                                "usuario": usuario,
                                "retornostream": response_text},
                                "chave":st.secrets["CHAVE"]}
                        if st.session_state.marcar_artigos == False:
                            data["data"]["pensador"] = st.session_state.selected_thinker
                        post_response = requests.post(url, json=data, timeout=5*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao acessar servidor: {e}")
                        st.stop()
                    #st.markdown(post_response.json())
                    client = OpenAI()
                    # Generate a response using the OpenAI API.
                    stream = client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=post_response.json().get("saida").get("mensagem"),
                    stream=True,
                    )
                    response_text = st.write_stream(stream)

                status.update(
                    label="Pesquisa por contra-argumentos completa.", state="complete", expanded=False
                )
                
            with pensamento4.status("Contra-Argumentação", expanded=True) as status:
                st.write("Desenvolvendo contra-argumentos.")
                with st.spinner("Aguarde.", show_time=True):
                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/artigos/continuar/"
                        url = f"http://52.2.202.37{caminho}/continuar/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"stream": 4,
                                "usuario": usuario,
                                "retornostream": response_text},
                                "chave":st.secrets["CHAVE"]}
                        if st.session_state.marcar_artigos == False:
                            data["data"]["pensador"] = st.session_state.selected_thinker
                        post_response = requests.post(url, json=data, timeout=5*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao acessar servidor: {e}")
                        st.stop()
                    #st.markdown(post_response.json())
                    client = OpenAI()
                    # Generate a response using the OpenAI API.
                    stream = client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=post_response.json().get("saida").get("mensagem"),
                    stream=True,
                    )
                    response_text = st.write_stream(stream)

                status.update(
                    label="Contra-Argumentos Completo.", state="complete", expanded=False
                )
            
            with st.spinner("Processando resposta final.", show_time=True): 
                try:
                    #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/artigos/continuar/"
                    url = f"http://52.2.202.37{caminho}/continuar/"
                    #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                    data = {"data":{"stream": 5,
                            "usuario": usuario,
                            "retornostream": response_text},
                            "chave":st.secrets["CHAVE"]}
                    if st.session_state.marcar_artigos == False:
                        data["data"]["pensador"] = st.session_state.selected_thinker
                    post_response = requests.post(url, json=data, timeout=5*60)
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao acessar servidor: {e}")
                    st.stop()
                #st.markdown(post_response.json())
                client = OpenAI()
                mensagens,argumentacao = post_response.json().get("saida").get("mensagem")
                # Generate a response using the OpenAI API.
                stream = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=mensagens,
                stream=True,
                )
                with pensamento6.status("Referências", expanded=False) as status:
                    st.write("Referências da Argumentação")
                    for parte in argumentacao.get("Referências da Argumentação").split("+=-!!-=+"):
                        st.write(parte)

                with pensamento7.status("Referências Contra-Argumentação", expanded=False) as status:
                    st.write("Referências do Contra-argumento")
                    for parte in argumentacao.get("Referências do Contra-argumento").split("+=-!!-=+"):
                        st.write(parte)
                    
                try:
                    #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/addartigostream/"
                    url = "http://52.2.202.37/produto/post/filosofo/addartigostream/"
                    #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                    data = {"data":{"usuario": st.session_state.usuario,
                                    "dados": argumentacao},
                                    "chave":st.secrets["CHAVE"]}
                    post_response = requests.post(url, json=data, timeout=5*60)
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao acessar servidor: {e}")
                    st.stop()
                
                with pensamento8.chat_message("assistant"):
                    response_text = st.write_stream(stream)
                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/addusuario/"
                        url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"usuario": st.session_state.usuario,
                                "entrada": prompt["text"],
                                "saida": response_text},
                                "chave":st.secrets["CHAVE"]}
                        post_response2 = requests.post(url, json=data, timeout=5*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao enviar os dados: {e}")
            try:
                #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/retornarconversa/"
                url = "http://52.2.202.37/produto/post/filosofo/retornarconversa/"
                #url = "http://52.2.202.37/produto/post/filosofo/retornarconversa/"
                data = {"data":{"usuario": st.session_state.usuario},"chave":st.secrets["CHAVE"]}
                st.session_state.messages = requests.post(url, json=data, timeout=5*60).json().get("saida")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao acessar servidor: {e}")
                st.stop()
            st.rerun(scope="app")
        else:

            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.

            # Chamada à API (substitua a URL pelo endpoint real) 
            
            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.

            #url = "http://52.2.202.37/produto/post/filosofo/chat/"
            #data = {"data":{"usuario": st.session_state.usuario,
            #        "mensagem": prompt["text"]}
            #        }
            #response = requests.post(url, json=data, timeout=5*60)
            #if response.status_code == 200:  
            #    saida = response.json().get("saida")
            #else:
            #    saida = str(response.status_code)+"\n\n"+str(response)
            #with st.chat_message("assistant"):
            #    st.markdown(str(saida))
            #    st.session_state.messages.append({"role": "assistant", "content": saida})
            with saidachat.container():
                with st.chat_message("assistant"):
                    #st.write(str(st.session_state.messages))
                    # Create an OpenAI client.
                    #client = OpenAI(api_key=openai_api_key)
                    
                    provisorio = []
                    for i in st.session_state.messages:
                        if i["role"] == "assistant":
                            provisorio.append(i)
                        elif i["role"] == "user":
                            provisorio.append(i)
                        elif i["role"] == "developer":
                            provisorio.append(i)
                        elif i["role"] == "ReferenciasArtigos":
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Pesquisa")}]})
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Pensamento")}]})
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Análise")}]})
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Contra-argumentos")}]})
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Referências da Argumentação")}]})
                            provisorio.append({'role': 'assistant', 'content': [{'type': 'text', 'text': i["content"][0]["text"].get("Referências do Contra-argumento")}]})
                            
                    client = OpenAI()
                    # Generate a response using the OpenAI API.
                    stream = client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=provisorio,
                    stream=True,
                    )
                    response_text = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": [{"type":"text","text":response_text}]}) 

                    try:
                        #url = "https://plainly-touched-ox.ngrok-free.app/produto/post/filosofo/addusuario/"
                        url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        #url = "http://52.2.202.37/produto/post/filosofo/addusuario/"
                        data = {"data":{"usuario": st.session_state.usuario,
                                "entrada": prompt["text"],
                                "saida": response_text},
                                "chave":st.secrets["CHAVE"]}
                        post_response = requests.post(url, json=data, timeout=5*60)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao enviar os dados: {e}")
                    st.rerun(scope="app")

            
        #st.session_state.marcar_artigos = False
        #st.rerun(scope="fragment")

x='''

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
                placeholder.markdown(st.session_state.chat_messages[-1]["content"])'''