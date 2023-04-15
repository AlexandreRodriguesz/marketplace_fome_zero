# Libries
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import numpy as np
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

#  home page
st.set_page_config( page_title="Main Page", layout='wide')

#==========================
# import dataset
#==========================
df = pd.read_csv('dataset/zomato.csv')

#==========================
# listas (países, cores)
#==========================
# países
COUTRIES = {
    1 : "India",
    14 : "Australia",
    30 : "Brazil",
    37 : "Canada",
    94 : "Indonesia",
    148 : "New Zeland",
    162 :"Philippines",
    166 : "Qatar",
    184 : "Singapure",
    189 : "South Africa",
    191 : "Sri Lanka",
    208 : "Turkey",
    214 : "United Arab Emirates",
    215 : "England",
    216 : "Unite States of America"
    
    }

# cores
COLORS = {
            "3F7E00" : "darkgreen",
            "5BA829" :  "grenn",
            "9ACD32" : "lightgreen",
            "CDD614" : "orange",
            "FFBA00" : "red",
            "FF7800" : "darkred",
            "CBCBC8" : "darkred"
        }

#==========================
# funções
#==========================

@st.cache_data
def convert_df(df1):
    """ Essa função cria um botão para download do csv.
    
    Input: arquivo csv
    Output: arquivo csv
        
    """
    return df1.to_csv().encode('utf-8')


def rename_colors(df):
    """ Essa função renomeia a coluna cor.

    Input: dataframe com a coluna cor com valores do tipo (int)
    Output: dataframe com a coluna cor renomeada (str)
    
    """
    df['cor'] = df['cor'].apply( lambda x:COLORS[x])
    df['cor'] = df['cor'].astype(str)
        
    return df


def country_name(df):
    """ Essa função renomeia a coluna country.
       
    Input: dataframe, coluna que receberá a mudança dos países
    Output: dataframe com a coluna selecionada renomeada
    
    """
    df['country'] = df['country'].apply( lambda x: COUTRIES[x])
    df['country'] = df['country'].astype(str)
    
    return df

 
def clean(df):
    """ Essa função faz a limpeza do dataframe.
    
    Input: dataframe
    Output: dataframe limpo
    
    """
    # retirando valores duplicados de todo o dataframe
    df_clean = df.drop_duplicates()

    # categorizando tipos culinários por apenas um tipo.
    df_clean['Cuisines'] = df.loc[:, 'Cuisines'].apply( lambda x: str(x).split(",")[0])

    # removendo dados nan da coluna 'Cuisines'
    filtro = df_clean['Cuisines'] != 'nan'
    df_clean = df_clean.loc[filtro, :]
  
    return df_clean


def rename(df):
    """ Essa função renomeia a coluna country.

    Input: dataframe
    Output:dataframe com a coluna country renomeada com os nomes dos países.
    
    """
    df_rename = df.rename(columns={'Restaurant ID': 'restaurant_ID', 'Restaurant Name' : 'nome_restaurant', 
                            'Country Code': 'country', 'Locality Verbose': 'locality_details', 'Average Cost for two' : 'mesa_dois',
                            'Has Table booking': 'reserva_mesa','Has Online delivery' : 'entrega_online' , 'Is delivering now' : 'entregando_agora' ,
                            'Switch to order menu' : 'mudar_menu_pedidos' , 'Price range' : 'faixa_preco' , 'Aggregate rating' : 'avaliacao_detalhada', 
                            'Rating color' : 'cor' , 'Rating text' : 'avaliacao' , 'Votes' : 'votos'})
    
    return df_rename

#==========================
# clean/rename
#==========================
df = clean(df)
df = rename(df)
df = country_name(df)
df = rename_colors(df)

#==========================
# dataframe clean
#==========================
df1 = df.copy()

#==========================
# barra lateral
#==========================
image = Image.open('logo.png')
st.sidebar.image(image, width=50)
st.sidebar.markdown('# Restaurante Fome zero')

st.sidebar.markdown('# Filtros')

# selecao paises
paises_options = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', 
                                        ['Philippines', 'Brazil', 'Australia', 'Unite States of America',
                                        'Canada', 'Singapure', 'United Arab Emirates', 'India',
                                        'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka',
                                        'Turkey'], default=['Philippines', 'Brazil', 'Australia',
                                                                          'Unite States of America',
                                                                          'Canada', 'Singapure', 'United Arab Emirates',
                                                                          'India','Indonesia', 'New Zeland', 'England', 
                                                                          'Qatar', 'South Africa','Sri Lanka', 'Turkey'])

# filtro selecao países
linhas_selecionadas = df1['country'].isin(paises_options)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""___""")
st.sidebar.markdown('# Dados tratados')

# botão p/ download dataframe
csv = convert_df(df1)
st.sidebar.download_button(
    label="Download data as csv",
    data=csv,
    file_name='dataset/zomato.csv',
    mime='text/csv',
)
st.sidebar.markdown("""___""")
st.sidebar.caption('### Powered by Comunidade DS')


#==========================
# layout central
#==========================
st.markdown('# Restaurante Fome Zero! ')
st.markdown('# Visão Geral')

st.markdown('## O melhor lugar para encontrar seu mais novo restaurante favorito!')

st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')
with st.container():
    #obs melhoras os nomes de cada item(não está aparecendo o nome todo)
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    
    # restaurantes cadastrados
    rest_ID = len(df1['restaurant_ID'].unique())
    col1.metric('Restaurantes cadastrados', rest_ID)
    
   
    # países cadastrados
    country_resg = len(df1['country'].unique())
    col2.metric('Países cadastrados', country_resg)
    
    # cidades cadastradas
    city_reg = len(df1['City'].unique())
    col3.metric('Cidades cadastradas', city_reg)
   
    # avaliações feitas na plataforma
    avaliacao_reg = df1['votos'].sum()
    col4.metric('Avaliações feitas na plataforma', avaliacao_reg)
       
    # tipos de culinárias oferecidas
    types_cuisines = len(df1['Cuisines'].unique())
    col5.metric('Tipos de culinárias oferecidas', types_cuisines)
        
with st.container():
    st.header('Visão geográfica dos restaurantes')
    
    cols = ['City', 'country' ,'restaurant_ID', 'Latitude', 'Longitude', 'cor']
    df_mapa = df1.loc[:, cols].groupby(['restaurant_ID','City','country']).median().reset_index()
    
    # create map
    map_ = folium.Map(zoom_start=11)
    # type marcação
    cluster = MarkerCluster().add_to(map_)
    
    for index, location in df_mapa.iterrows():
        folium.Marker([location['Latitude'],
                       location['Longitude']],
                      icon=folium.Icon(color='cor', icon='home', prefix='fa'),
                      popup=location[['City', 'restaurant_ID']]).add_to(cluster)
        
    folium_static(map_, width=1024, height=600)    
    
  
