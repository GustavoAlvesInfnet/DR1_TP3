import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt


# Criar um sidebar
st.sidebar.title("Personalização")

# Opção de cor de fundo
cor_fundo = st.sidebar.color_picker("Selecione uma cor de fundo", "#00000F")

# Opção de cor de texto
cor_texto = st.sidebar.color_picker("Selecione uma cor de texto", "#FFFFFF")

# Aplicar as opções de personalização
st.markdown(f"<style>.main {{background-color: {cor_fundo}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<style>p {{color: {cor_texto}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<style>h3 {{color: {cor_texto}; }}</style>", unsafe_allow_html=True)


url = "https://www.data.rio/documents/45fa86aa30374bfabd369e6d64179071/about"



# link
st.subheader("Link usado:")
st.write(url)

st.subheader("Selecione o arquivo xls ou xlsx que deseja do portal Data.Rio:")

uploaded_file = st.file_uploader("Escolha o arquivo", type=["xls", "xlsx"])



if uploaded_file is not None:
    progress_bar = st.progress(0)
    # Crie um spinner
    with st.spinner("Carregando dados..."):

        df = pd.read_excel(uploaded_file)
        df = df.iloc[7:69]
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        #Muda o nome das colunas
        df.columns = ['Continentes e países de residência permanente', 'total', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        #st.write(df.head())

        # Selecção de colunas
        colunas = df.columns.tolist()
        colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas, default=colunas)
        df_selecionado = df[colunas_selecionadas]
        # muda a ordem das colunas, deixa o total primeiro e os paises depois
        df_selecionado = df_selecionado.reindex(columns=["total", "Continentes e países de residência permanente",  "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"])


        # Filtro de linhas
        filtro = st.selectbox("Selecione o tipo de filtro:", ["Nenhum", "Maior que", "Menor que", "Igual a"])
        if filtro != "Nenhum":
            coluna_filtro = st.selectbox("Selecione a coluna para filtrar:", df_selecionado.columns)
            valor_filtro = st.number_input("Digite o valor para filtrar:")
            if filtro == "Maior que":
                df_filtrado = df_selecionado[df_selecionado[coluna_filtro] > valor_filtro]
            elif filtro == "Menor que":
                df_filtrado = df_selecionado[df_selecionado[coluna_filtro] < valor_filtro]
            elif filtro == "Igual a":
                df_filtrado = df_selecionado[df_selecionado[coluna_filtro] == valor_filtro]

        else:
            df_filtrado = df_selecionado

        for i in range(100):
            # Atualize a barra de progresso
            progress_bar.progress(i + 1)
            # Simule o processamento dos dados
            time.sleep(0.01)

    # Visualização dos dados
    st.write(df_filtrado)

    # Grafico com dados filtrados, usando os dados filtrados, países e total (sem os meses)

    fig, ax = plt.subplots(figsize=(6, 12))
    ax.barh(range(len(df_filtrado['Continentes e países de residência permanente'])), df_filtrado['total'])
    ax.set_ylabel('Continentes e países de residência permanente')
    ax.set_xlabel('Total')
    ax.set_yticks(range(len(df_filtrado['Continentes e países de residência permanente'])))
    ax.set_yticklabels(df_filtrado['Continentes e países de residência permanente'])
    st.pyplot(fig)


    #dowload dos dados filtrados
    if st.button("Download"):
        st.download_button(
            label="Download",
            data=df_filtrado.to_csv(index=False),
            file_name="dados_filtrados.csv",
            mime="text/csv",
        )


else:
    # Mostra uma mensagem de espera
    st.write("Aguardando arquivo...")
    st.spinner("Carregando...")






