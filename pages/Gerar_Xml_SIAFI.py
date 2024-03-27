import streamlit as st
import pandas as pd
from datetime import datetime
import io

xml_counter = 1  # Definir xml_counter globalmente

def generate_xml(df, ano_referencia, cpf_responsavel, txt_processo, txt_obser):
    global xml_counter  # Declarar xml_counter como global para poder modificá-lo

    df['cpf'] = df['cpf'].astype(str).str.zfill(11)
    df['valor'] = df['valor'].astype(float)
    aggregated_data = df.groupby('cpf')['valor'].sum()

    numSeqItem_counter = 1
    cpf_list = []

    dt_emis = datetime.now().strftime('%Y-%m-%d')
    dt_ateste = datetime.now().strftime('%Y-%m-%d')

    xml_files = []

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
          <dtEmis>{dt_emis}</dtEmis>
          <codUgPgto>120093</codUgPgto>
          <vlr>{total:.2f}</vlr>
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
          <vlr>{valor_cpf:.2f}</vlr>
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

            xml_files.append(xml_content)
            xml_counter += 1
            cpf_list = []

    return xml_files

def format_currency(value):
    # Formata o valor como moeda local
    return "${:,.2f}".format(value)

def main():
    st.title('App de Geração de XML')

    uploaded_file = st.file_uploader("Faça upload de uma planilha Excel", type=['xlsx'])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, names=['saram', 'cpf', 'posto', 'nome', 'valor', 'mes_ano'])  # Definir nomes das colunas explicitamente

        # Formatando as colunas
        df['saram'] = df['saram'].astype(str)
        df['cpf'] = df['cpf'].astype(str).str.zfill(11)

        st.write(df)

        st.write("---")
        total_value = df['valor'].sum()
        st.write(f"Total: {format_currency(total_value)}")  # Mostrar a soma total da coluna 'valor' formatada

        st.write("---")
        st.subheader("Preencha os campos abaixo:")
        ano_referencia = st.text_input("Ano de Referência", value=str(datetime.now().year))
        cpf_responsavel = st.text_input("CPF do Responsável")
        txt_processo = st.text_input("Texto do Processo")
        txt_obser = "RELATÓRIO DOS MILITARES EM MISSÃO NO EXTERIOR - MÊS DE MARÇO DE 2024"

        if st.button("Gerar XML"):
            if not df.empty:
                xml_files = generate_xml(df, ano_referencia, cpf_responsavel, txt_processo, txt_obser)
                st.success("XMLs gerados com sucesso!")

                # Exibir botões de download para os XMLs gerados
                st.write("---")
                st.subheader("Baixar XMLs Gerados:")
                for i, xml_content in enumerate(xml_files):
                    xml_filename = f'XML_{i+1}.xml'
                    xml_io = io.BytesIO(str.encode(xml_content))
                    st.download_button(label=f'Baixar {xml_filename}', data=xml_io, file_name=xml_filename)
            else:
                st.error("O arquivo Excel está vazio. Por favor, faça upload de um arquivo com dados.")
                
if __name__ == "__main__":
    main()