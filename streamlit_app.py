import streamlit as st
#from openai import OpenAI
import requests
import warnings

def ativar_artigos():
    if st.session_state.marcar_artigos:
        st.session_state.marcar_pensadores = False
        if st.session_state.selected_thinker:
            st.session_state.selected_thinker = None

def ativar_pensadores():
    if st.session_state.marcar_pensadores:
        st.session_state.marcar_artigos = False
        if st.session_state.selected_thinker is None:
            st.session_state.selected_thinker = "Sócrates"

# Suppress Streamlit's ScriptRunContext warning
warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# Configuração inicial da página
st.set_page_config(page_title="O Pensador Desktop", layout="wide")

st.title("💬 O Pensador Desktop")
#st.write("ssssssss")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
if "openai_api_entered" not in st.session_state:
    st.session_state.openai_api_key = st.text_input("Senha", type="password")
    st.session_state.openai_api_entered = True
else:
    openai_api_key = st.session_state.openai_api_key
    coluna1, coluna2  = st.columns([2, 6], border=True)
    # Create an OpenAI client.
    #client = OpenAI(api_key=openai_api_key)
    with coluna1:
        # Cria duas colunas: a primeira para o checkbox e a segunda para o ícone de informação
        col_checkbox, col_info = st.columns([0.9, 0.1])

        with col_checkbox:
            st.subheader("Ferramentas")
            marcarArtigos = st.checkbox(
                "Artigos Científicos", 
                value=False, 
                key="marcar_artigos", 
                on_change=ativar_artigos
            )
        with col_info:
            # Define o texto que aparecerá ao passar o mouse
            info_text = "Selecioneasdasdasdasdasdasdasd"
            # O ícone ℹ (código HTML &#9432;) possui o atributo title que exibe o tooltip
            st.markdown(
                f"<span title='{info_text}' style='cursor: pointer;'>&#9432;</span>",
                unsafe_allow_html=True
            )


        marcarPensador = st.checkbox(
            "Pensadores", 
            value=False, 
            key="marcar_pensadores", 
            on_change=ativar_pensadores
        )
        
        if "selected_thinker" not in st.session_state:
            st.session_state.selected_thinker = None

        if st.session_state.marcar_artigos:
            st.write("Modo 'Artigos Científicos' ativado.")
        elif st.session_state.marcar_pensadores:
            st.session_state.selected_thinker = st.selectbox(
                "Selecione o pensador:",
                options=["Sócrates", "Platão", "Aristóteles", "Descartes"],
                index=["Sócrates", "Platão", "Aristóteles", "Descartes"].index(st.session_state.selected_thinker)
            )
            st.write("Modo 'Pensadores' ativado.")
        else:
            st.write("Nenhum modo ativo.")            
            
        if st.session_state.marcar_pensadores:
            st.info("Artigos desativados", icon="⚠️")
        if st.session_state.marcar_artigos:
            st.info("Pensadores desativados", icon="⚠️")
    with coluna2:
        # Create a session state variable to store the chat messages. This ensures that the
        # messages persist across reruns.
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Create a chat input field to allow the user to enter a message. This will display
        # automatically at the bottom of the page.
        if prompt := st.chat_input("Em que eu posso te ajudar?"):

            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            
            # Generate a response using the OpenAI API.
            #stream = client.chat.completions.create(
            #    model="gpt-3.5-turbo",
            #    messages=[
            #        {"role": m["role"], "content": m["content"]}
            #        for m in st.session_state.messages
            #    ],
            #    stream=True,
            #)

            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.
            #with st.chat_message("assistant"):
            #    response = st.write_stream(stream)
            try:
                # Chamada à API (substitua a URL pelo endpoint real)
                url = "http://52.2.202.37/teste/"
                data = {"cliente": "string",
                        "produto": "string",
                        }
                response = requests.post(url, json=data, timeout=5*60)
                if response.status_code == 200:  
                    saida = response.json()["saida"]
                    print(saida)
                    erro = response.json()["erro"]
                    print(erro)
                else:  
                    print("Erro na requisição")
                    print(response.status_code)
                    print(response.text) 
                    st.stop()   
            except Exception as e:
                dados = {"mensagem": "Erro ao processar a mensagem."}
            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.

            with st.chat_message("assistant"):
                st.markdown(saida)
            if st.session_state.marcar_pensadores:
                st.session_state.messages.append({"role": "assistant", "content": saida})
            if st.session_state.marcar_artigos:
                st.session_state.messages.append({"role": "assistant", "content": saida})
            
            #st.session_state.messages.append({"role": "assistant", "content": response})

        
