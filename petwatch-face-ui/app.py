import streamlit as st
from lmodel.dashboard import Dash
from lmodel.cat_collections import CollectionSelector
from lmodel.verify import Verify

def main():
    # Configuração da página
    st.set_page_config(layout='wide')

    # Título
    st.title('🐱 Petwatch Face Recognize 🐱')
    st.sidebar.title('Gestão de Pet')
    st.sidebar.write("---")

    # Menu de seleção
    menu = st.sidebar.selectbox(
        'Menu:',
        (
            "Verificar",
            "Dashboard",
            "Cat Collections",
        )
    )

    # Seção Cat Collections
    if menu == 'Cat Collections':
        CollectionSelector.seletor()

    # Seção Verificar
    if menu == "Verificar":
        Verify.verificar_gato()

    # Seção Dashboard
    if menu == 'Dashboard':
        Dash.exibir_dashboard()

if __name__ == "__main__":
    main()