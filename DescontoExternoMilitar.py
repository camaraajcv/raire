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
    # Lê o arquivo PDF e extrai o texto em blocos
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())

    # Define padrões de regex para extrair informações específicas
    padrao_inicio = re.compile(r'H01\s+([0-9,.]+)\s+([A-Z0-9\s-]+)\n')
    padrao_acantus = re.compile(r'([A-Z]{1}[0-9A-Z]+)\s+([0-9,.]+)\s+([A-Z0-9\s-]+)\n')

    # Inicializa uma lista para armazenar os resultados
    resultados = []

    # Lê o arquivo PDF em blocos
    with fitz.open(temp_file.name) as pdf_doc:
        num_paginas = pdf_doc.page_count
        for pagina_num in range(num_paginas):
            pagina = pdf_doc[pagina_num]
            texto_pagina = pagina.get_text()

            # Encontrar o padrão "H01" para iniciar a busca
            inicio_match = padrao_inicio.search(texto_pagina)
            if inicio_match:
                valor_inicial, descricao_inicial = inicio_match.groups()
                resultados.append(("H01", valor_inicial, descricao_inicial))
                
                # Extrair padrões subsequentes a partir de "H01"
                matches = padrao_acantus.findall(texto_pagina[inicio_match.end():])
                resultados.extend(matches)

    # Exibe os resultados
    for match in resultados:
        st.write(f"Padrão: {match[0]}, Valor: {match[1]}, Descrição: {match[2]}")