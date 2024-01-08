import re
import pandas as pd
import fitz
import io
import tempfile
import streamlit as st
import os
from datetime import datetime
# Adiciona um título à barra lateral
st.sidebar.title("Descontos Externos")

# Adiciona um link para o outro aplicativo Streamlit
link_militar = "[Militar](/workspaces/streamlit-example/streamlit_app_mil.py)"
link_civil = "[Civil](/workspaces/streamlit-example/streamlit_app.py)"

st.sidebar.markdown(link_militar, unsafe_allow_html=True)
st.sidebar.markdown(link_civil, unsafe_allow_html=True)
# URL da imagem
image_url = "https://www.fab.mil.br/om/logo/mini/dirad2.jpg"

#Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'

data_geracao = datetime.now().strftime('%Y-%m-%d')
data_geracao2 = datetime.now().strftime('%d/%m/%Y')


# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)


# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.2em;'>SUBDIRETORIA DE PAGAMENTO DE PESSOAL</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1em; text-decoration: underline;'>PP1 - DIVISÃO DE DESCONTOS</h3>", unsafe_allow_html=True)

# Texto explicativo
st.write("Desconto Externo Militar - Extração dados PDF SIGPES para SIAFI")

# Adiciona um botão para fazer upload do arquivo PDF
uploaded_file = st.file_uploader("Faça o upload do arquivo PDF", type="pdf")

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    # Lê o arquivo PDF e extrai o texto
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())

    with fitz.open(temp_file.name) as pdf_doc:
        num_paginas = pdf_doc.page_count
        texto_pdf = ""
        for pagina_num in range(num_paginas):
            pagina = pdf_doc[pagina_num]
            texto_pdf += pagina.get_text()

    # Define padrões de regex para extrair informações específicas
    padrao_codigo_despesa = re.compile(r'CÓD\. DO ELEMENTO DESPESA:(.*?)\n', re.DOTALL)
    padrao_descricao = re.compile(r'DESCR[IAÇÃO]+:(.*?)\n', re.DOTALL)

    # Extrai as informações usando regex
    codigos_despesa = padrao_codigo_despesa.findall(texto_pdf)
    descricoes = padrao_descricao.findall(texto_pdf)

    # Exibe as informações extraídas
    st.write("CÓD. DO ELEMENTO DESPESA:")
    st.write(codigos_despesa)

    st.write("DESCRIÇÃO:")
    st.write(descricoes)