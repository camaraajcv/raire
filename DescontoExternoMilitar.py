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


    # Dicionário de dados contendo país, posto e fator de conversão
    data = {
        "Afeganistão": {"Cabul - FCG": 85.28},
        "África do Sul": {"Cidade do Cabo - FCG": 45.11, "Pretória": 47.32},
        "Albânia": {"Tirana": 51.52},
        "Alemanha": {"Frankfurt": 66.78, "Munique": 66.78, "Berlim - FCG": 68.94},
        "Angola": {"Luanda - FCG": 86.58},
        "Antártica": {"Antártica": 99.86},
        "Arábia Saudita": {"Riade": 66.24, "Jeddah (Jiddah) - FCG": 66.24},
        "Argélia": {"Argel - FCG": 57.60},
        "Argentina": {"Buenos Aires": 58.38, "Mendoza": 42.25, "Paso de Los Libres": 45.20, "Puerto Iguazu": 45.20, "Córdoba - FCG": 42.25},
        "Armênia": {"Ierevan": 60.80},
        "Austrália": {"Camberra - FCG": 67.50, "Sidney": 67.86},
        "Áustria": {"Viena - FCG": 75.39},
        "Azerbaijão": {"Baku": 73.60},
        "Bahamas": {"Nassau - FCG": 72.45},
        "Bahrein": {"Manama": 57.78},
        "Bangladesh": {"Daca": 56.64},
        "Barbados": {"Bridgetown": 45.24},
        "Belarus": {"Minsk": 52.32},
        "Bélgica": {"Bruxelas - FCG": 72.24},
        "Belize": {"Belmopán": 52.78},
        "Benin": {"Cotonou - FCG": 65.76},
        "Bolívia": {"Cobija": 43.00, "Cochabamba": 43.00, "Guayaramerin": 43.00, "Puerto Suarez": 43.00, "Santa Cruz de la Sierra": 68.80, "La Paz - FCG": 59.58},
        "Bósnia e Herzegovina": {"Sarajevo": 53.12},
        "Botsuana": {"Gaborone": 60.80},
        "Bulgária": {"Sófia - FCG": 47.06},
        "Burkina Faso": {"Uagadugu": 67.52},
        "Cabo Verde": {"Praia - FCG": 65.34},
        "Camarões": {"Iaundê": 70.08},
        "Camboja": {"Phnom Pehn - FCG": 53.09},
        "Canadá": {"Ottawa": 63.18, "Toronto": 59.68, "Vancouver": 59.68, "Montreal - FCG": 59.04},
        "Catar": {"Doha": 57.78},
        "Cazaquistão": {"Astana": 59.84},
        "Chile": {"Santiago - FCG": 59.58},
        "China": {"Chengdu": 73.07, "Hong-Kong": 77.49, "Pequim": 80.22, "Xangai": 74.52, "Cantão - FCG": 71.64},
        "Chipre": {"Nicósia": 54.86},
        "Cingapura": {"Cingapura - FCG": 66.30},
        "Colômbia": {"Letícia": 54.21, "Bogotá - FCG": 50.57},
        "República Democrática do Congo": {"Kinshasa - FCG": 77.49},
        "República do Congo": {"Brazzaville": 90.30},
        "Coreia do Norte": {"Pyongyang": 71.82},
        "Coreia do Sul": {"Seul": 59.76, "Inchon - FCG": 53.12},
        "Croácia": {"Zagreb": 51.61},
        "Costa do Marfim": {"Abdijã - FCG": 76.68},
        "Costa Rica": {"São José": 43.94},
        "Cuba": {"Havana - FCG": 62.08},
        "Dinamarca": {"Copenhague - FCG": 80.64},
        "Egito": {"Cairo - FCG": 51.74},
        "El Salvador": {"São Salvador": 43.94},
        "Emirados Árabes Unidos": {"Abu Dábi": 66.24},
        "Equador": {"Quito - FCG": 40.56},
        "Eslováquia": {"Bratislava": 67.52},
        "Eslovênia": {"Liubliana": 50.44},
        "Espanha": {"Madrid": 64.80, "Barcelona - FCG": 54.34},
        "Estônia": {"Talin": 66.96},
        "Etiópia": {"Adis-Abeba": 63.00},
        "EUA": {"Atlanta": 59.85, "Chicago": 64.89, "Hartford": 61.95, "Houston": 59.85, "Los Angeles": 66.15, "Miami": 63.42, "Nova York": 78.52, "Orlando": 63.42, "São Francisco": 64.89, "Washington": 76.70, "Boston - FCG": 61.95, "San Juan (Porto Rico)": 61.95},
        "Filipinas": {"Manila - FCG": 52.80},
        "Finlândia": {"Helsinki - FCG": 62.72},
        "França": {"Marselha": 82.68, "Paris - FCG": 82.68},
        "Gabão": {"Libreville": 93.66},
        "Gana": {"Acra": 66.72},
        "Geórgia": {"Tbilisi": 60.80},
        "Grécia": {"Atenas - FCG": 62.08},
        "Guatemala": {"Guatemala": 47.32},
        "Guiana": {"Lethem": 54.21, "Georgetown - FCG": 57.76},
        "Guiana Francesa": {"Saint Georges de l’Oyapock": 66.88, "Caiena - FCG": 66.88},
        "Guiné": {"Conacri": 61.92},
        "Guiné Bissau": {"Bissau": 72.72},
        "Guiné Equatorial": {"Malabo": 73.44},
        "Haiti": {"Porto Príncipe- FCG": 65.44},
        "Honduras": {"Tegucigalpa - FCG": 43.94},
        "Hungria": {"Budapeste - FCG": 53.17},
        "Índia": {"Nova Délhi - FCG": 50.18, "Mumbai": 50.18},
        "Indonésia": {"Jacarta - FCG": 64.68},
        "Irã": {"Teerã": 51.04},
        "Iraque": {"Bagdá": 85.28},
        "Irlanda": {"Dublin - FCG": 74.55},
        "Israel": {"Tel-Aviv - FCG": 66.24},
        "Itália": {"Roma - FCG": 69.48, "Milão": 67.52},
        "Jamaica": {"Kingston - FCG": 49.66},
        "Japão": {"Tóquio": 108.94, "Hamamatsu": 82.62, "Nagoya - FCG": 82.62},
        "Jordânia": {"Amã": 55.51},
        "Kuaite": {"Kuaite": 57.78},
        "Líbano": {"Beirute - FCG": 63.00},
        "Líbia": {"Trípoli - FCG": 51.84},
        "Malásia": {"Kuala Lumpur - FCG": 64.47},
        "Maláui": {"Lilongue": 52.78},
        "Mali": {"Bamako": 65.44},
        "Marrocos": {"Rabat - FCG": 48.36},
        "Mauritânia": {"Nouakchott": 67.52},
        "México": {"México - FCG": 57.12},
        "Myanmar": {"Yangon": 56.80},
        "Moçambique": {"Maputo - FCG": 63.72},
        "Namíbia": {"Windhoek - FCG": 62.46},
        "Nepal": {"Katmandu": 56.64},
        "Nicarágua": {"Manágua": 49.60},
        "Nigéria": {"Abuja": 75.81, "Lagos - FCG": 75.81},
        "Noruega": {"Oslo - FCG": 73.98},
        "Nova Zelândia": {"Wellington - FCG": 51.09},
        "Omã": {"Mascate": 57.78},
        "Cisjordânia": {"Ramalá": 69.12},
        "Panamá": {"Panamá - FCG": 51.52},
        "Paquistão": {"Islamabad - FCG": 62.88},
        "Países Baixos": {"Haia": 70.77, "Amsterdã - FCG": 77.75, "Rotterdam": 61.92},
        "Paraguai": {"Assunção": 52.74, "Ciudad del Este": 42.64, "Concepción - FCG": 47.70, "Encarnación": 58.11, "Pedro Juan Caballero": 36.30, "Salto del Guaira": 47.70},
        "Peru": {"Lima": 44.72, "Cusco": 40.70, "Iquitos - FCG": 40.70},
        "Polônia": {"Varsóvia - FCG": 54.88},
        "Portugal": {"Lisboa": 63.00, "Faro": 52.78, "Porto - FCG": 52.78},
        "Quênia": {"Nairóbi": 52.52},
        "Reino Unido": {"Edimburgo": 78.89, "Londres - FCG": 78.89},
        "República Dominicana": {"São Domingos - FCG": 51.52},
        "República Tcheca": {"Praga - FCG": 52.65},
        "Romênia": {"Bucareste": 45.50},
        "Ruanda": {"Kigali": 75.63},
        "Rússia": {"Moscou - FCG": 65.76},
        "Santa Lúcia": {"Castries": 44.59},
        "Santa Sé": {"Vaticano": 69.48},
        "São Tomé e Príncipe": {"São Tomé": 59.22},
        "São Vicente e Granadinas": {"Kingstown": 44.59},
        "Senegal": {"Dacar": 67.52},
        "Sérvia": {"Belgrado": 47.06},
        "Serra Leoa": {"Freetown": 83.34},
        "Síria": {"Damasco - FCG": 67.84},
        "Sri Lanka": {"Colombo": 50.18},
        "Sudão": {"Cartum - FCG": 63.84},
        "Sudão do Sul": {"Juba - FCG": 63.84},
        "Suécia": {"Estocolmo - FCG": 64.80},
        "Suíça": {"Berna - FCG": 81.18, "Genebra": 103.48, "Zurique": 84.96},
        "Suriname": {"Paramaribo": 59.84},
        "Tailândia": {"Bangkok": 57.28},
        "Taiwan, Província da China": {"Taipé": 108.94},
        "Tanzânia": {"Dar-es-Salaam": 52.78},
        "Timor Leste": {"Díli - FCG": 70.14},
        "Togo": {"Lomé": 68.80},
        "Trinidad e Tobago": {"Port-of-Spain": 57.98},
        "Tunísia": {"Túnis - FCG": 42.90},
        "Turquia": {"Ancara - FCG": 47.32, "Istambul": 51.61},
        "Ucrânia": {"Kiev - FCG": 52.32},
        "Uruguai": {"Montevidéu - FCG": 49.28, "Artigas": 47.50, "Chuy": 36.30, "Rio Branco": 47.50, "Rivera": 35.40},
        "Venezuela": {"Caracas - FCG": 75.67, "Ciudad Guayana": 67.32, "Puerto Ayacucho": 75.06, "Santa Elena de Uairén": 75.06},
        "Vietnã": {"Hanói": 63.21},
        "Zâmbia": {"Lusaca": 54.60},
        "Zimbábue": {"Harare": 64.80}
    }

    # Criando os seletor de país e posto
    selected_country = st.selectbox("Selecione o país", list(data.keys()))
    selected_post = st.selectbox("Selecione o posto", list(data[selected_country].keys()))

    # Obtendo o fator de conversão para o posto selecionado
    conversion_factor = data[selected_country][selected_post]

    # Mostrando o fator de conversão
    st.success(f"Fator de Conversão para {selected_post}: {conversion_factor}")
    # Seletor de datas
start_date = st.date_input("Selecione a data de início:")
end_date = st.date_input("Selecione a data de término:")

# Botão para calcular a quantidade de dias
if st.button("Calcular"):
    # Calcula a diferença entre as datas
    delta = end_date - start_date
    # Exibe a quantidade de dias
    st.write(f"A quantidade de dias entre {start_date.strftime('%d/%m/%Y')} e {end_date.strftime('%d/%m/%Y')} é: {delta.days} dias.")
    # Converter o dicionário em um DataFrame
rr = pd.DataFrame(data)

# Exibir o DataFrame
rr

from streamlit.components.v1 import components

# Adicionando um componente personalizado para seleção de intervalo de tempo
date_range = components.date_input(
    label="Selecione o intervalo de tempo:",
    key="date_range",
    value=("2022-01-01", "2022-12-31"),  # Intervalo de tempo padrão
    help="Selecione o intervalo de tempo desejado."
)

# Exibindo o intervalo de tempo selecionado
st.write("Intervalo de tempo selecionado:", date_range)