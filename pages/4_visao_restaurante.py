# Libries
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
import numpy as np
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Restaurante', layout='wide')
#==========================
# import dataset
#==========================
df = pd.read_csv('dataset/zomato.csv')

#==========================
# listas (Países, cores)
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
# Funções
#==========================

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
    Output: dataframe clean
    
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
    df_clean = df.rename(columns={'Restaurant ID': 'restaurant_ID', 'Restaurant Name' : 'nome_restaurant', 
                            'Country Code': 'country', 'Locality Verbose': 'locality_details', 'Average Cost for two' : 'mesa_dois',
                            'Has Table booking': 'reserva_mesa','Has Online delivery' : 'entrega_online' , 'Is delivering now' : 'entregando_agora' ,
                            'Switch to order menu' : 'mudar_menu_pedidos' , 'Price range' : 'faixa_preco' , 'Aggregate rating' : 'avaliacao_detalhada', 
                            'Rating color' : 'cor' , 'Rating text' : 'avaliacao' , 'Votes' : 'votos'})
    
    return df_clean

def top_culin(df1, asc_to):
    """ Essa função mostra um top 10 dos melhores ou dos piores restaurantes culinários.

    Parametros:
               asc_to=True : mostra os piores restaurantes
               asc_to_False : mostra os melhores restaurantes

    Input: dataframe and value bool
    Output: Gráfico com o top 10 dos restaurantes
    
    """
    if asc_to == True:
        filtro = df1.loc[:, 'avaliacao_detalhada'] > 0
        df1 = df1.loc[filtro, :]
        
       
    df_aux01 = ( df1.loc[:, ['votos', 'avaliacao_detalhada', 'Cuisines', 'country']]
                    .groupby(['Cuisines', 'country'])
                    .mean()
                    .sort_values('avaliacao_detalhada', ascending=asc_to)
                    .head(10)
                    .reset_index() )
        
    fig = px.bar(df_aux01, x='Cuisines', y='avaliacao_detalhada')
        
    return fig

def create_price_tye(faixa_valor):
    """ Essa função transforma os valores de faixa de preço (int) em (str)palavras,
        para descrever melhor a faixa de preço.
    
        Parametros: valor 1 == "cheap" 
                    valor 2 == "normal"
                    valor 3 == "expensive"
                    valor 4 == "gourmet"
                    
    Input: valores da coluna "faixa_preco"
    Output: valores e tipo str               
    
   """
    if faixa_valor == 1:
        return "cheap"
    elif faixa_valor == 2:
        return "normal"
    elif faixa_valor == 3:
        return "expensive"
    else:
        return "gourmet"
    
def m_rest(df1):   
    df_aux = (df1.loc[:, ['avaliacao_detalhada', 'nome_restaurant', 'Cuisines']]
                     .groupby(['nome_restaurant', 'Cuisines'])
                     .mean()
                     .sort_values('avaliacao_detalhada', ascending=False)
                     .reset_index() )
    
    return df_aux
    
    
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
st.sidebar.markdown('# Filtro')

image = Image.open('logo.png')
st.sidebar.image(image, width=60)

# selecao países
paises_options = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', 
                                        ['Philippines', 'Brazil', 'Australia', 'Unite States of America',
                                        'Canada', 'Singapure', 'United Arab Emirates', 'India',
                                        'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka',
                                        'Turkey'], default=['Philippines', 'Brazil', 'Australia',
                                                                          'Unite States of America',
                                                                          'Canada', 'Singapure', 'United Arab Emirates',
                                                                          'India','Indonesia', 'New Zeland', 'England', 
                                                                          'Qatar', 'South Africa','Sri Lanka', 'Turkey'])

# filtro selecao de países
linhas_selecionadas = df1['country'].isin(paises_options)
df1 = df1.loc[linhas_selecionadas, :]

# filtro slider selecao de restaurante
df_filtro = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar', 
                           value= 10
                           ,
                           min_value= 1, 
                           max_value= 20)
df1 = df1.head(df_filtro)


#==========================
# layout central
#==========================
st.title('Visão Restaurantes')

with st.container():
    st.markdown('# Melhores restaurantes dos principais tipos de culinária')
    col1, col2, col3, col4, col5 = st.columns( 5 )
    
    df_top_r = m_rest(df1)
    
    if df_filtro >= 1:
       col1.metric(label=str(df_top_r.loc[0, 'Cuisines']) + '/' + str(df_top_r.loc[0, 'nome_restaurant']),
                   value=float(df_top_r.loc[0,'avaliacao_detalhada'])) 
    if df_filtro >= 2:
       col2.metric(label=str(df_top_r.loc[1, 'Cuisines']) + '/' + str(df_top_r.loc[1, 'nome_restaurant']),
                   value=float(df_top_r.loc[1,'avaliacao_detalhada'])) 
    if df_filtro >= 3:
       col3.metric(label=str(df_top_r.loc[2, 'Cuisines']) + '/' + str(df_top_r.loc[2, 'nome_restaurant']),
                   value=float(df_top_r.loc[2,'avaliacao_detalhada'])) 
    if df_filtro >= 4:
       col4.metric(label=str(df_top_r.loc[3, 'Cuisines']) + '/' + str(df_top_r.loc[3, 'nome_restaurant']),
                   value=float(df_top_r.loc[3,'avaliacao_detalhada'])) 
    if df_filtro >= 5:
       col5.metric(label=str(df_top_r.loc[4, 'Cuisines']) + '/' + str(df_top_r.loc[4, 'nome_restaurant']), 
                   value=float(df_top_r.loc[4,'avaliacao_detalhada'])) 
        
with st.container():
     st.markdown('## Os 10 Melhores restaurantes com maior avaliação') 
     df1 = df1.drop(columns=['entregando_agora', 'mudar_menu_pedidos'])
     df1['faixa_preco'] = df1.loc[:, 'faixa_preco'].apply( lambda x: create_price_tye(x))
     df_top10 = df1.sort_values('avaliacao_detalhada', ascending=False).head(10).reset_index()
     st.dataframe(df_top10, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2, gap='large')    
    
    with col1:
        st.markdown('## Top 10 Melhores Tipos de Culinárias')
        df_top_culin = top_culin(df1, asc_to=False)
        st.plotly_chart(df_top_culin, use_container_width=True)
        
    with col2:
        st.markdown('## Top 10 Piores Tipos de culinárias')  
        df_top10_culin_02 = top_culin(df1, asc_to=True)
        st.plotly_chart(df_top10_culin_02, use_container_width=True)
    
   