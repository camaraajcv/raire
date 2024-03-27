import streamlit as st
import pandas as pd
from datetime import datetime
# URL da imagem
image_url = "https://www.fab.mil.br/om/logo/mini/dirad2.jpg"

#Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'
# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)

# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.2em;'>SUBDIRETORIA DE PAGAMENTO DE PESSOAL</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1em; text-decoration: underline;'>PP2 - DIVISÃO DE PAGAMENTO DE PESSOAL NO EXTERIOR</h3>", unsafe_allow_html=True)

# Texto explicativo
st.write("Gerando XML para o SIAFI")
def generate_xml(df, ano_referencia, cpf_responsavel, txt_processo, txt_obser):
    df['cpf'] = df['CPF'].astype(str).str.zfill(11)
    df['valor'] = df['Valor'].round(2)
    aggregated_data = df.groupby('cpf')['valor'].sum()

    numSeqItem_counter = 1
    xml_counter = 1
    cpf_list = []

    dt_emis = datetime.now().strftime('%d/%m/%Y')
    dt_ateste = datetime.now().strftime('%Y-%m-%d')

    for cpf, valor in aggregated_data.items():
        cpf_list.append(cpf)
        if len(cpf_list) == 100 or cpf == aggregated_data.index[-1]:
            total = sum(aggregated_data[cpf] for cpf in cpf_list).round(2)
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sb:arquivo xmlns:sb="http://www.tesouro.gov.br/siafi/submissao">
  <sb:header>
    <sb:codigoLayout>DH001</sb:codigoLayout>
    <sb:dataGeracao>{dt_emis}</sb:dataGeracao>
    <sb:sequencialGeracao>{xml_counter}</sb:sequencialGeracao>
    <sb:anoReferencia>{ano_referencia}</sb:anoReferencia>
    <sb:ugResponsavel>120093</sb:ugResponsavel>
    <sb:cpfResponsavel>{cpf_responsavel}</sb:cpfResponsavel>
  </sb:header>
  <sb:detalhes>
    <sb:detalhe>
      <ns2:CprDhCadastrar xmlns:ns2="http://services.docHabil.cpr.siafi.tesouro.fazenda.gov.br/">
        <codUgEmit>120093</codUgEmit>
        <anoDH>{ano_referencia}</anoDH>
        <codTipoDH>RC</codTipoDH>
        <dadosBasicos>
          <dtEmis>{dt_ateste}</dtEmis>
          <codUgPgto>120093</codUgPgto>
          <vlr>{total}</vlr>
          <txtObser>{txt_obser}</txtObser>
          <txtProcesso>{txt_processo}</txtProcesso>
          <dtAteste>{dt_ateste}</dtAteste>
          <codCredorDevedor>120093</codCredorDevedor>
        </dadosBasicos>"""

            for cpf in cpf_list:
                valor_cpf = aggregated_data[cpf]
                xml_content += f"""
        <outrosLanc>
          <numSeqItem>{numSeqItem_counter}</numSeqItem>
          <codSit>LDV014</codSit>
          <vlr>{valor_cpf}</vlr>
          <txtInscrA>{cpf}</txtInscrA>
          <numClassA>899910700</numClassA>
        </outrosLanc>"""
                numSeqItem_counter += 1

            xml_content += """
      </ns2:CprDhCadastrar>
    </sb:detalhe>
  </sb:detalhes>
  <sb:trailler>
    <sb:quantidadeDetalhe>1</sb:quantidadeDetalhe>
  </sb:trailler>
</sb:arquivo>"""

            with open(f'XML_{xml_counter}.xml', 'w') as f:
                f.write(xml_content)

            xml_counter += 1
            cpf_list = []

def main():
    st.title('App de Geração de XML')

    uploaded_file = st.file_uploader("Faça upload de uma planilha Excel", type=['xlsx'])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write(df)

        # Manter apenas as colunas relevantes
        df = df[['CPF', 'Valor']]

        st.write("---")
        st.subheader("Preencha os campos abaixo:")
        ano_referencia = st.text_input("Ano de Referência", value=str(datetime.now().year))
        cpf_responsavel = st.text_input("CPF do Responsável")
        txt_processo = st.text_input("Texto do Processo")
        txt_obser = "RELATÓRIO DOS MILITARES EM MISSÃO NO EXTERIOR - MÊS DE MARÇO DE 2024"

        if st.button("Gerar XML"):
            generate_xml(df, ano_referencia, cpf_responsavel, txt_processo, txt_obser)
            st.success("XMLs gerados com sucesso!")

if __name__ == "__main__":
    main()