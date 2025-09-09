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
    st.markdown("""
    <style>
    div.stButton {text-align: center;}
    </style>
    """, unsafe_allow_html=True)
    if st.button("Entrar"):
        st.switch_page("login.py")