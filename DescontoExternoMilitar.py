import re
import pandas as pd
import fitz
import io
import tempfile
import streamlit as st
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

# Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'

data_geracao = datetime.now().strftime('%Y-%m-%d')
data_geracao2 = datetime.now().strftime('%d/%m/%Y')

# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)

# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA DO RODOLFO</h1>", unsafe_allow_html=True)
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

    # Inicializa uma lista para armazenar os dados extraídos
    dados_extraidos = []

    # Inicializa a variável para indicar se "H01" foi encontrado
    h01_encontrado = False

    # Inicializa listas para armazenar os dados específicos
    cx_acantus = []

    # Lê o arquivo PDF em blocos
    with fitz.open(temp_file.name) as pdf_doc:
        num_paginas = pdf_doc.page_count
        for pagina_num in range(num_paginas):
            pagina = pdf_doc[pagina_num]
            texto_pagina = pagina.get_text()

            # Adiciona o texto da página à lista
            dados_extraidos.append(texto_pagina)

            # Verifica se "H01" foi encontrado na linha
            if re.search(r'\bH01\b', texto_pagina):
                h01_encontrado = True

            if h01_encontrado:
                # Busca todos os padrões de 3 caracteres que atendem à condição
                matches_tres_caracteres = re.findall(r'\b([A-Z][0-9A-Z]{2}[0-9A-Z])\b', texto_pagina)

                # Filtra para garantir que tenhamos 3 dígitos, com o primeiro sendo uma letra
                matches_tres_caracteres = [match for match in matches_tres_caracteres if re.match(r'^[A-Z][0-9A-Z]{2}$', match)]

                # Adiciona os demais padrões à lista
                cx_acantus.extend(matches_tres_caracteres)

    # Concatena todo o texto em uma única linha
    dados_em_linha = ' '.join(dados_extraidos)

    # Exibe todo o texto extraído
    st.write("Todos os dados extraídos do PDF em uma única linha:")
    st.write(dados_em_linha)

    # Cria um DataFrame com os dados extraídos da coluna "CX ACANTUS"
    df_cx_acantus = pd.DataFrame({"CX ACANTUS": cx_acantus})

    # Exibe o DataFrame
    st.write("DataFrame 'CX ACANTUS' gerado a partir dos dados extraídos:")
    st.write(df_cx_acantus)

