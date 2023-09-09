import streamlit as st
import pandas as pd
import numpy as np
from requests import get

class Dash(object):

    @staticmethod
    def exibir_dashboard():
        
        endpoint = "http://localhost:5000/inferencia/status"
        response = get(endpoint).json()

        st.sidebar.image("src/uly_2.png")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Informações do Serviço')
            url = 'http://localhost:5001/gatos'
        
            response_api = get(url).json()
            df_api = pd.DataFrame.from_dict(response_api)
            grid, grid1 = st.columns(2)
            with grid:
              st.metric(label="Total Gatos Cadastrados", value=len(df_api))
            with grid1:  
              st.metric(label="Modelo Produtivo", value=response['model'][0])
            
            st.table(df_api)


            df = pd.DataFrame.from_dict(response['success_logs'])
                   # Combina as colunas 'date' e 'hour' em uma única coluna 'timestamp'
            df['timestamp'] = df['date'] + ' ' + df['hour']

            # Convertendo a coluna 'timestamp' para tipo datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Calculando a contagem de requisições por minuto
            df['count'] = 1
            df.set_index('timestamp', inplace=True)
            resampled_data = df.resample('T').sum()

            # Identificando o minuto com o máximo e o mínimo de requisições
            minuto_maximo = resampled_data['count'].idxmax()
            maximo_requisicoes = resampled_data['count'].max()
            minuto_minimo = resampled_data['count'].idxmin()
            minimo_requisicoes = resampled_data['count'].min()

            # Criando gráficos
            st.info(f'Min Máximo de Requisições ({maximo_requisicoes} requisições): {minuto_maximo}')
            st.warning(f'Min Mínimo de Requisições ({minimo_requisicoes} requisições): {minuto_minimo}')



        with col2:
            st.subheader('Requisições')

            metric, metric1 = st.columns(2)
            with metric:
                st.metric(label="Total Success", value=response['success_count']['count'])
            with metric1:
                st.metric(label="Total Error", value=response['error_count']['count'])
            
            df = pd.DataFrame.from_dict(response['success_logs'])
            
            # Combina as colunas 'date' e 'hour' em uma única coluna 'timestamp'
            df['timestamp'] = df['date'] + ' ' + df['hour']

            # Converte a coluna 'timestamp' para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Agrupa os dados por minuto e conta o número de ocorrências em cada minuto
            grouped = df.groupby(pd.Grouper(key='timestamp', freq='1Min')).size().reset_index(name='count')

            # Cria um gráfico de linha
            st.subheader('Contagem de Requisições por Minuto')
            st.line_chart(grouped.set_index('timestamp'))

        st.subheader('Logs')
        st.table(df.head(20))