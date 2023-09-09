import streamlit as st
import pandas as pd
from requests import post, get


class Verify(object):

    @staticmethod
    def verificar_gato():
        st.sidebar.image("src/SamPoderoso.png")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.file_uploader('File uploader')
            latitude = -22.936426
            longitude = -47.093800

            if st.button('Verificar'):
                st.table({"Nome": "Uly", "Idade": "4 anos", "Tutores": "Debora Rodrigues e Juan Manoel",
                          "Localidade": "Campinas SP", "CEP": "123456678", 'Contato': "+55 41 992149181"})
                with col2:
                    st.image("saida.jpg")
                with col3:
                    map = pd.DataFrame.from_dict([{"LAT": latitude, "LONG": longitude}])
                    st.map(map, latitude='LAT', longitude='LONG', zoom=17, size=10)

