import streamlit as st
from openai import OpenAI
import requests
import warnings
from PIL import Image
import time
from time import sleep
# Suppress Streamlit's ScriptRunContext warning
warnings.filterwarnings("ignore", message="missing ScriptRunContext")
st.set_page_config(page_title="O Pensador Desktop", layout="wide")

if "selected_thinker" not in st.session_state:
    st.session_state.selected_thinker = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def Carregando(aceleracao=0.1):
    porcentagem = 0
    cols = st.columns(3)
    with cols[1]:
        my_bar = st.progress(porcentagem, text="Iniciando plataforma...")
        tempo=0.5
        
        url = "https://plainly-touched-ox.ngrok-free.app/filosofo/retornarconversa/"
        #url = "http://52.2.202.37/filosofo/retornarconversa/"
        data = {"data":{"usuario": int(st.session_state.usuario)}}
        st.session_state.messages = requests.post(url, json=data, timeout=5*60).json().get("saida")
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
        sleep(tempo)
        
        porcentagem += 25
        my_bar.progress(porcentagem, text="Finalizando...")
        tempo+=aceleracao
        sleep(tempo)
        my_bar.empty()

    st.session_state.carregado = True
    st.rerun(scope="app")


@st.dialog("Entrar")
def Entrar():
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        cols2 = st.columns([1,1,1,1,1])
        with cols2[2]:
            submit_login = st.form_submit_button("Entrar")
        if submit_login and usuario.strip() and senha.strip():
            st.session_state.usuario = usuario
            st.session_state.senha = senha
            st.session_state.carregado = False
            st.session_state.product_page = "home"
            st.rerun(scope="app")

@st.dialog("Criar Usuário")
def Cadastrar():
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        cols2 = st.columns([1,1,1,1,1])
        with cols2[2]:
            submit_login = st.form_submit_button("Entrar")
        if submit_login and usuario.strip() and senha.strip():
            st.session_state.usuario = usuario
            st.session_state.senha = senha

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
            st.session_state.selected_thinker = "Sócrates"


#st.write("ssssssss")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management



#cols = st.columns([5, 1])
#with cols[1]:
#    cols2 = st.columns([1, 1])
#    with cols2[0]:
#        if st.button("Login", key="login_button"):
#            Entrar()
#    with cols2[1]:
#        if st.button("Sign Up", key="signup_button"):
#            Cadastrar() 

if "usuario" not in st.session_state:
    cols = st.columns(3)
    with cols[1]:
        cols3 = st.columns(3)
        with cols3[1]:
            image = Image.open("dados/exemplo/imagem.jpg")
            st.image(image, use_container_width=True)
    
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; font-weight: bold;">
                💬 O Pensador Desktop
            </div>
            """,
            unsafe_allow_html=True
        )
        cols = st.columns(3)
        with cols[1]:
            if st.button("Login", key="login_button",use_container_width=True):
                Entrar()
            if st.button("Sign Up", key="signup_button",use_container_width=True):
                Cadastrar()
        

    
    #st.title("💬 O Pensador Desktop") 
    
    #st.session_state.openai_api_key = st.text_input("Senha", type="password")
    #st.session_state.openai_api_entered = True

elif st.session_state.usuario and st.session_state.product_page == "chat":
    # Menu do chat
    #opcoeschat = st.columns(5, vertical_alignment="center")
    # Cria o checkbox e o ícone de informação na mesma linha
    col = st.columns([1, 1, 1, 1, 1, 2], vertical_alignment="top")
    with col[0]:
        # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
        col_checkbox, col_info = st.columns([0.7, 0.3])
        # Cria o checkbox e o ícone de informação na mesma linha
        with col_checkbox:
            marcarArtigos = st.checkbox(
                "Artigos", 
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
    with col[1]:
        # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
        col_checkbox, col_info = st.columns([0.7, 0.3])
        # Cria o checkbox e o ícone de informação na mesma linha
        with col_checkbox:
            # Cria o checkbox para o modo "Pensadores" e o ícone de informação na mesma linha
            marcarPensador = st.checkbox(
                "Pensadores", 
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
    with col[3]:
        if st.button("Limpar Chat", use_container_width=True):
            url = "https://plainly-touched-ox.ngrok-free.app/filosofo/recomecarconversa/"
            #url = "http://52.2.202.37/filosofo/recomecarconversa/"
            data = {"data":{"usuario": int(st.session_state.usuario)}
                    }
            requests.post(url, json=data, timeout=5*60).json().get("saida")

            st.session_state.messages = []
            st.rerun(scope="app")
    with col[2]:
        if st.button("Menu", use_container_width=True):
            st.session_state.product_page = "home"
            st.rerun(scope="app")
    with col[5]:
        if not st.session_state.marcar_pensadores and not st.session_state.marcar_artigos:
            if "selected_model" not in st.session_state or st.session_state.selected_model not in ["gpt-4o-mini", "gpt-4o", "o3-mini"]:
                st.session_state.selected_model = "gpt-4o-mini"
            
            
            model_keys = ["gpt-4o-mini", "gpt-4o", "o3-mini"]
            model_names = {
                "gpt-4o-mini": "Gpt-4o-mini: Resposta rápida para tarefas leves.",
                "gpt-4o": "Gpt-4o: Resposta rápida para tarefas com média complexidade.",
                "o3-mini": "O3-mini: Modelo de pensamento para tarefas mais complexas"
            }
            selected = st.selectbox(
                "Motor do chat:",
                options=model_keys,
                index=model_keys.index(st.session_state.selected_model),
                format_func=lambda key: model_names[key]
            )
            st.session_state.selected_model = selected
    
    with col[5]:
        #if st.session_state.marcar_artigos:
        #    st.write("Artigos ativado.")
        if st.session_state.marcar_pensadores:
            st.session_state.selected_thinker = st.selectbox(
                "Selecione o pensador:",
                options=["Sócrates", "Platão", "Aristóteles", "Descartes"],
                index=["Sócrates", "Platão", "Aristóteles", "Descartes"].index(st.session_state.selected_thinker)
            )
    with st.container(height=400,border=False):
            with st.container():
                if not st.session_state.carregado:
                    Carregando()
                else:
                    url = "https://plainly-touched-ox.ngrok-free.app/filosofo/retornarconversa/"
                    #url = "http://52.2.202.37/filosofo/retornarconversa/"
                    data = {"data":{"usuario": int(st.session_state.usuario)}
                            }
                    st.session_state.messages = requests.post(url, json=data, timeout=5*60).json().get("saida")
                #openai_api_key = st.session_state.openai_api_key
                
                
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
                        else:
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"][0]["text"])
                                #st.markdown(message["content"][0].get("text"))

                entradachat = st.empty()
                saidachat = st.empty()
                # Create a chat input field to allow the user to enter a message. This will display
                # automatically at the bottom of the page.
                if prompt := st.chat_input("Em que eu posso te ajudar?",accept_file=True,file_type=["jpg", "jpeg", "png","pdf","mp3"],):

                    # Store and display the current prompt.
                    st.session_state.messages.append({"role": "user", "content": prompt["text"]})
                    with entradachat.container():
                        with st.chat_message("user"):
                            st.markdown(prompt["text"])

                    
                    #with st.status("Processando..."):
                    #    time.sleep(0.5)
                    #    st.write("Pesquisando informação...")
                    #    time.sleep(0.5)
                    #    st.write("Aprimorando resposta...")
                    #    time.sleep(0.5)
                    #    st.write("Finalizando...")
                    #    time.sleep(0.5)

                    # Stream the response to the chat using `st.write_stream`, then store it in 
                    # session state.

                    # Chamada à API (substitua a URL pelo endpoint real) 
                    
                    # Stream the response to the chat using `st.write_stream`, then store it in 
                    # session state.

                    #url = "http://52.2.202.37/filosofo/chat/"
                    #data = {"data":{"usuario": int(st.session_state.usuario),
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
                            st.session_state.messages.append({"role": "user", "content": prompt["text"]})
                            # Create an OpenAI client.
                            #client = OpenAI(api_key=openai_api_key)

                            client = OpenAI()
                            # Generate a response using the OpenAI API.
                            stream = client.chat.completions.create(
                            model=st.session_state.selected_model,
                            messages=st.session_state.messages,
                            stream=True,
                            )
                            response_text = st.write_stream(stream)

                            url = "https://plainly-touched-ox.ngrok-free.app/filosofo/addusuario/"
                            #url = "http://52.2.202.37/filosofo/addusuario/"
                            data = {"data":{"usuario": int(st.session_state.usuario),
                                    "entrada": prompt["text"],
                                    "saida": response_text}
                                    }
                            post_response = requests.post(url, json=data, timeout=5*60)
            
elif st.session_state.usuario and st.session_state.product_page == "loja":
    st.subheader("Loja")
    cols = st.columns(3)
    
    #st.markdown(
    #    """
    #    <style>
    #    div.stButton > button {
    #        height: 150px;
    #        min-height: 150px;
    #    }
    #    </style>
    #    """,
    #    unsafe_allow_html=True
    #)

    with cols[0]:
        if st.button('Você poderá realizar +40 interações com o chat e mais +10 Consultas nos Livros.',icon = "⚡", key="plan1", use_container_width=True):
            st.success("Plano Básico selecionado")

    with cols[1]:
        if st.button("Você poderá realizar +30 Consultas nos Livros.",icon = "🔥", key="plan2", use_container_width=True):
            st.success("Plano Intermediário selecionado")

    with cols[2]:
        if st.button("Você poderá realizar +70 Consultas nos Livros.",icon = "💎", key="plan3", use_container_width=True):
            st.success("Plano Premium selecionado")
            
    # Lembre-se de fechar o container após os botões:
    st.markdown('''</div>''', unsafe_allow_html=True)

    # Exemplo de lista de pagamentos com id, valor, status e link
    payments = [
        {"id": "P001", "valor": "100.00", "status": "Link Gerado", "link": "https://example.com/payment/P001"},
        {"id": "P002", "valor": "200.00", "status": "Processando", "link": "https://example.com/payment/P002"},
        {"id": "P003", "valor": "300.00", "status": "Aprovado", "link": "https://example.com/payment/P003"},
        {"id": "P004", "valor": "400.00", "status": "Cancelado", "link": "https://example.com/payment/P004"},
    ]

    def render_status_button(status, link):
        # Define a cor do botão conforme o status: "Aprovado" e "Link Gerado" verde,
        # "Processando Pagamento" amarelo e "Cancelado" vermelho.
        if status in ["Processando", "Link Gerado"]:
            color = "#B8860B"  # dark goldenrod, a darker yellow
        elif status == "Aprovado":
            color = "green"
        elif status == "Cancelado":
            color = "red"
        else:
            color = "gray"
        # Cria um botão que redireciona para o link indicado
        button_html = f"""
        <div style="text-align: center;">
            <a href="{link}" target="_blank">
                <button style="background-color: {color}; color: white; border: none; padding: 5px 10px; border-radius: 4px;">
                    {status}
                </button>
            </a>
        </div>
        """
        return button_html

    st.subheader("Lista de Pagamentos")
    # Exibe os pagamentos em linhas com três colunas: id, valor e status (botão)
        
    col_id, col_valor, col_status = st.columns([1, 1, 1])
    with col_id:
        st.write("Código de Pagamento")
    with col_valor:
        st.write(f"Valor")
    with col_status:
        status_button = render_status_button("Atualizar Pagamentos", "https://chatbot-filosofo.streamlit.app/")
        st.markdown(status_button, unsafe_allow_html=True)
    st.markdown("---")
    for idx, payment in enumerate(payments):
        col_id, col_valor, col_status = st.columns([1, 1, 1])
        with col_id:
            st.write(payment["id"])
        with col_valor:
            st.write(f"R$ {payment['valor']}")
        with col_status:
            status_button = render_status_button(payment["status"], payment["link"])
            st.markdown(status_button, unsafe_allow_html=True)
        if idx < len(payments) - 1:
            st.markdown("---")

elif st.session_state.usuario and st.session_state.product_page == "home":
    # Adiciona uma variável de controle para a página atual se ainda não existir
    #st.markdown(
    #    """
    #    <div style="text-align: center;">
    #        <h1>Olá 😊</h1>
    #    </div>
    #    """,
    #    unsafe_allow_html=True
    #)

    # Cria quatro colunas para os produtos
        
    col = st.columns([1,1,1,1,1,2],vertical_alignment="center")

    with col[2]:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.product_page = "chat"
            st.rerun(scope="app")
        # Define o texto que aparecerá ao passar o mouse
        info_text1 = "Um assistente que se adapta a você! Com capacidade de ler e processar PDFs, imagens e  áudios com precisão, tudo em uma única ferramenta inteligente que facilita o acesso a informações essenciais, otimiza seu fluxo de trabalho e impulsiona sua criatividade em qualquer tarefa."
        # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip 
        st.markdown(
        f"""
        <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
            <span title="{info_text1}" style="cursor: pointer; font-size: 18px;">&#9432;</span>
        </div>
        """,
        unsafe_allow_html=True
        )
        
    #with col2:
    #    # Define o texto que aparecerá ao passar o mouse
    #    info_text2 = "Com mais de 220 mil artigos da Arxiv (Base de dados mantida pela Cornell University) do ano de 2024. Superando as limitações dos modelos atuais treinados com informações até outubro de 2023. Além de proporcionar uma melhora da qualidade das respostas e apresentando referências para ser validadas. Isto tem como objetivo de ter um mecanismo de pesquisa imparcial."
    #    # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
    #    st.markdown(
    #    f"""
    #    <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
    #        <span title="{info_text2}" style="cursor: pointer; font-size: 18px;">&#9432;</span>
    #    </div>
    #    """,
    #    unsafe_allow_html=True
    #    )
    #    if st.button("📚 Artigos Científicos", use_container_width=True):
    #        st.session_state.product_page = "artigos"
        
    #with col3:
    #    # Define o texto que aparecerá ao passar o mouse
    #    info_text3 = """Tenha uma inteligência artificial treinada nas obras de diversos pensadores. Desbrave o mundo das ideias e encontre respostas para os seus questionamentos mais difíceis."""
    #    # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
    #    st.markdown(
    #    f"""
    #    <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
    #        <span title="{info_text3}" style="cursor: pointer; font-size: 18px;">&#9432;</span>
    #    </div>
    #    """,
    #    unsafe_allow_html=True
    #    )
    #    if st.button("🤔 Filósofos", use_container_width=True):
    #        st.session_state.product_page = "filosofos"
        

    with col[3]:
        if st.button("🗣 Mesa de discussão", use_container_width=True):
            st.session_state.product_page = "mesa_discussao"
            st.rerun(scope="app")
        # Define o texto que aparecerá ao passar o mouse
        info_text4 = """A mesa de discussão reúne quatro filósofos para analisar um tema em seis etapas: fatos, emoções, pontos negativos, pontos positivos, visões alternativas e, por fim, a organização das ideias. Essa abordagem garante um debate equilibrado e multidimensional, onde cada aspecto do tema é explorado de forma clara e estruturada."""
        # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
        st.markdown(
        f"""
        <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
            <span title="{info_text4}" style="cursor: pointer; font-size: 18px;">&#9432;</span>
        </div>
        """,
        unsafe_allow_html=True
        )
    with col[4]:
        if st.button("Loja", use_container_width=True):
            st.session_state.product_page = "loja"
            st.rerun(scope="app")
        # Define o texto que aparecerá ao passar o mouse
        info_text1 = "Uma loja com produtos e serviços que podem ser adquiridos com o uso de créditos. Os créditos podem ser comprados diretamente na loja."
        # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip 
        st.markdown(
        f"""
        <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
            <span title="{info_text1}" style="cursor: pointer; font-size: 18px;">&#9432;</span>
        </div>
        """,
        unsafe_allow_html=True
        )




