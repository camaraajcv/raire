import re
import pandas as pd
import fitz
import io
import tempfile
import streamlit as st
from datetime import datetime
import tabula

# ... (seu código anterior)

# Adiciona um botão para fazer upload do arquivo PDF
uploaded_file = st.file_uploader("Faça o upload do arquivo PDF", type="pdf")

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    # Lê o arquivo PDF e extrai o texto em blocos
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())

    # Inicializa uma lista para armazenar os dados extraídos
    dados_extraidos = []

    # Inicializa uma lista para armazenar os dados da coluna "CX ACANTUS"
    cx_acantus = []

    # Lê o arquivo PDF em blocos
    with fitz.open(temp_file.name) as pdf_doc:
        num_paginas = pdf_doc.page_count
        for pagina_num in range(num_paginas):
            pagina = pdf_doc[pagina_num]
            texto_pagina = pagina.get_text()

            # Adiciona o texto da página à lista
            dados_extraidos.append(texto_pagina)

            # Encontra a primeira ocorrência de "H01" na linha
            match_h01 = re.search(r'\bH01\b', texto_pagina)
            if match_h01:
                # Extrai os demais padrões de 3 caracteres que atendem à condição
                matches_tres_caracteres = re.findall(r'\b([A-Z]{1}[0-9A-Z]{2}[0-9A-Z])\b', texto_pagina[match_h01.start():])

                # Filtra para garantir que tenhamos 3 dígitos, com o primeiro sendo uma letra
                matches_tres_caracteres = [match for match in matches_tres_caracteres if re.match(r'^[A-Z][0-9A-Z]{2}$', match)]

                cx_acantus.extend(["H01"] + matches_tres_caracteres)

    # Concatena todo o texto em uma única linha e exibe
    dados_em_linha = ' '.join(dados_extraidos)
    st.write("Todos os dados extraídos do PDF em uma única linha:")
    st.write(dados_em_linha)

    # Cria um DataFrame com os dados extraídos
    df = pd.DataFrame({"CX ACANTUS": cx_acantus})

    # Exibe o DataFrame
    st.write("DataFrame gerado a partir dos dados extraídos:")
    st.write(df)

    # Adiciona uma seção para análise com Tabula
    st.header("Análise com Tabula")

    # Adiciona um botão para executar a análise com Tabula
    if st.button("Executar análise com Tabula"):
        # Utiliza o Tabula para extrair tabelas do PDF
        try:
            tabula_df = tabula.read_pdf(temp_file.name, pages='all', multiple_tables=True)
            st.write("Tabelas extraídas com sucesso usando Tabula:")
            st.write(tabula_df)
        except Exception as e:
            st.write(f"Erro ao usar Tabula: {e}")
