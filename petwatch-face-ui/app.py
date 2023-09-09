import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium as f
from cat_collector import *
from streamlit_option_menu import option_menu

st.set_page_config(layout='wide')

st.title('🐱 Petwatch Face Recognize 🐱')
st.sidebar.title('Gestão de Pet')
st.sidebar.write("---")
menu = st.sidebar.selectbox('Menu:',
                 (
                  "Dashboard",
                  "Verificar",
                  "Cat Collections", 
                  )
                )

if menu == 'Cat Collections':
    #st.sidebar.video('ja_verificou.mp4', format="video/mp4", start_time=0)
    st.sidebar.markdown("![Alt Text](https://raw.githubusercontent.com/juanengml/Petwatch-Monitoring-System/main/petwatch-face-ui/ezgif-1-c06d2fccba.gif)")
    
    menu = option_menu(None, ["Cadastrar", "Status", "Deletar", 'Atualizar'], 
    icons=['Cadastrar', 'Status', "Deletar", 'Atualizar'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

    

    if menu == "Cadastrar":
        cadastra()
    elif menu == "Status":
        status()
    elif menu == "Atualizar":
        update()
    elif menu == "Deletar":
        deleter()

if menu == "Verificar":
    st.sidebar.image("SamPoderoso.png")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.file_uploader('File uploader')
        latitude = -22.936426
        longitude = -47.093800


        if st.button('Verificar'):
           st.table({"Nome": "Uly", "Idade": "4 anos", "Tutores": "Debora Rodrigues e Juan Manoel", "Localidade": "Campinas SP", "CEP": "123456678", 'Contato':"+55 41 992149181"})
           with col2: 
              st.image("saida.jpg")
           with col3: 
              # Coordenadas do ponto que você deseja marcar no mapa
              latitude = -22.936426
              longitude = -47.093800

              # Usando st.map para criar o mapa com o ponto
              map = pd.DataFrame.from_dict([{"LAT":latitude, "LONG":longitude}])
              st.map(map, latitude='LAT', longitude='LONG', zoom=17,size=10)




if menu == 'Dashboard':
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
