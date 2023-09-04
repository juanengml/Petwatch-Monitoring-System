import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide')

st.title('🐱 Petwatch Face Recognize 🐱')
st.sidebar.title('Gestão de Pet')

st.sidebar.radio('Menu:',
                 ["Dashboard",
                  "Verificar",
                  "Face Collections"]
                )
st.sidebar.image("uly_2.png")

col1, col2 = st.columns(2)

with col1:
    st.subheader('Informações do Serviço')
     
    data = {
        "Models": ["Haarcascade and cat detector svm"],
        "Service Name": ["Petwatch Face Recognize"],
        "Create on": ["03-09-2023"]
    }

    df = pd.DataFrame(data)


    st.table(data)
    # Criando dados aleatórios para os dias do mês (de segunda a domingo)
    classificacoes = ["Deteções", "Reconhecidos"]
    dados = np.random.randint(10, 25, 2)

    # Criando um DataFrame para os dados com uma coluna numérica para representar os dias da semana
    data = {"label": classificacoes, "Total": dados}
    df = pd.DataFrame(data)
    st.bar_chart(df, x='label', y='Total',color = ['#309c8f'])


with col2:
    st.subheader('Coleções de Faces')

    metric, metric1 = st.columns(2)
    with metric:
        st.metric(label="Total Images", value="23")
    with metric1:  
        st.metric(label="Total Cat Faces", value="45")
  

    # Criando dados aleatórios para os dias do mês (de segunda a domingo)
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dados = np.random.randint(10, 25, 7)

    # Criando um DataFrame para os dados com uma coluna numérica para representar os dias da semana
    data = {"Dia da Semana": dias_semana, "Total": dados}
    df = pd.DataFrame(data)

    
    # Plotando o gráfico de linha
    st.line_chart(df, x="Dia da Semana", y='Total')
