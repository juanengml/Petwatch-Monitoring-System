import streamlit as st
import pandas as pd
import numpy as np

class Dash(object):

    @staticmethod
    def exibir_dashboard():
        st.sidebar.image("src/uly_2.png")
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

            classificacoes = ["Deteções", "Reconhecidos"]
            dados = np.random.randint(10, 25, 2)
            data = {"label": classificacoes, "Total": dados}
            df = pd.DataFrame(data)
            st.bar_chart(df, x='label', y='Total', color=['#309c8f'])

        with col2:
            st.subheader('Coleções de Faces')

            metric, metric1 = st.columns(2)
            with metric:
                st.metric(label="Total Images", value="23")
            with metric1:
                st.metric(label="Total Cat Faces", value="45")

            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            dados = np.random.randint(10, 25, 7)
            data = {"Dia da Semana": dias_semana, "Total": dados}
            df = pd.DataFrame(data)

            st.line_chart(df, x="Dia da Semana", y='Total')

