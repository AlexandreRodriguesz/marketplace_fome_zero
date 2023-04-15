import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home"
    )


image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown( '# Fome Zero' )
st.sidebar.markdown( """___""")

st.write( '# Fome Zero Company Growth Dashboard' )

st.markdown(
    """
       Growth Dashboard foi construido para acompanhar as métricas de crescimento da empresa.
       ### Como utilizar esse Growth de comportamento?
         - Visão geral:
             - Métricas gerais dos restaurantes.
             - Insights de geolocalização.
         - Visão Cidades:
             - Acompanhamento dos indicadores de crescimento dos restaurantes e média de avaliação.
         - Visão Países:
             - Acompanhamento dos indicadores de crescimento dos restaurantes e média de avaliação.
         - Visão Restaurantes:
             - Ranking de avaliações dos melhores restaurantes e tipos culinários.  
        ### ASk for Help
        - Time de Data Science do Discord
            - @r_alexandre
    """
)