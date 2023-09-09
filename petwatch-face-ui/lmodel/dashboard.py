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
            df_api['data_nascimento'] = pd.to_datetime(df_api['data_nascimento'], format='%d/%m/%Y')
            df_api['ano_nascimento'] = df_api['data_nascimento'].dt.year
            
            grid, grid1 = st.columns(2)
            with grid:
                st.metric(label="Total Gatos Cadastrados", value=len(df_api))
                
                # Calcule a idade média dos gatos
                idade_media = (pd.to_datetime('today').year - df_api['ano_nascimento']).mean()

                # Crie um aplicativo streamlit para mostrar a idade média
                
                st.metric('Idade Média dos Gatos', value=f'{int(idade_media)} anos')
            with grid1:  
                st.metric(label="Modelo Produtivo", value=response['model'][0])
                df_api['ano_nascimento'] = df_api['data_nascimento'].dt.year
                # Converta a coluna 'create_at' para o formato datetime
                df_api['create_at'] = pd.to_datetime(df_api['create_at'])

                # Encontre a data de criação máxima e mínima
                data_maxima = df_api['create_at'].max()
                data_minima = df_api['create_at'].min()
                st.write("Ultimo registro: ", data_maxima)
                st.write("Primeiro registro: ", data_minima)


            
            st.table(df_api[['nome', 'ano_nascimento', 'image']])

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