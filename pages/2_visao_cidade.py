# Libries
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import numpy as np
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Cidade', layout='wide')

#=======================
# import dataset
#=======================
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

#=======================
# funções
#=======================

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
    """ Essa função faz a limpeza do dataframe
    
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
                            'Country Code': 'country', 'Locality Verbose': 'locality_details', 'Average Cost for two' : 'custo_medio_P_dois',
                            'Has Table booking': 'reserva_mesa','Has Online delivery' : 'entrega_online' , 'Is delivering now' : 'entregando_agora' ,
                            'Switch to order menu' : 'mudar_menu_pedidos' , 'Price range' : 'faixa_preco' , 'Aggregate rating' : 'avaliacao_detalhada', 
                            'Rating color' : 'cor' , 'Rating text' : 'avaliacao' , 'Votes' : 'votos'})
    
    return df_rename


def media_avaliacao(df, asc_to):
    """ Essa função mostra os países, com base na coluna avaliação_detalhada.

    parametros:
               asc_to=False : mostra os países com avaliação acima de 4.
               asc_to=True : mostra os países com avaliação abaixo de 2.5.
    Input: dataframe
    Output: Gráfico de barras com o países.           
    
    """
    if asc_to == False:
        df2 = df1['avaliacao_detalhada'] >= 4
    elif asc_to == True:
        df2 = df1['avaliacao_detalhada'] <= 2.5
            
    df_2 = ( df1.loc[:, ['avaliacao_detalhada', 'City', 'country']]
                .groupby(['City', 'country'])
                .mean()
                .sort_values('avaliacao_detalhada', ascending=asc_to)
                .head(7)
                .reset_index())
      
    fig = px.bar(df_2, x='City', y='avaliacao_detalhada', color='country', text_auto=True)
                    
    return fig


def top_city(df):
    """ Essa função mostra um top 10 de cidades que contém mais restaurantes.

    Input: dataframe
    Output: Gráfico de baras com as 10 cidades com mais restaurantes.
    
    """
    df_cities = ( df1.loc[:, ['restaurant_ID', 'City', 'country']]
                     .groupby(['City', 'country'])
                     .count()
                     .sort_values('restaurant_ID', ascending=False)
                     .head(10)
                     .reset_index() )
    
    fig = px.bar(df_cities, x='City', y='restaurant_ID', color='country', text_auto=True)
    
    return fig


def top_culin(df):   
    """ Essa função mostra um top de 10 de cidades que contém mais tipos culinários distintos.

    Input: dataframe
    Output: Gráfico de barras com as 10 cidades com mais tipos culinários distintos.
    
    """
    # nova coluna 'num_especialidades', com o número de tipos culinarios dos restaurantes.
    df1['num_especialidades'] = df1['Cuisines'].apply( lambda x: len(str(x).split(",")))
        
    df_aux = ( df1[['nome_restaurant', 'City', 'country','num_especialidades']].groupby(['City', 'country'])
                                                                               .sum()
                                                                               .sort_values('num_especialidades', ascending=False)
                                                                               .reset_index()
                                                                               .head(10) )
        
    fig = px.bar(df_aux, x='City', y='num_especialidades', color='country', text_auto=True)
        
    return fig


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

# seleção de países
paises_options = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', 
                                        ['Philippines', 'Brazil', 'Australia', 'Unite States of America',
                                        'Canada', 'Singapure', 'United Arab Emirates', 'India',
                                        'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka',
                                        'Turkey'], default=['Philippines', 'Brazil', 'Australia',
                                                                          'Unite States of America',
                                                                          'Canada', 'Singapure', 'United Arab Emirates',
                                                                          'India','Indonesia', 'New Zeland', 'England', 
                                                                          'Qatar', 'South Africa','Sri Lanka', 'Turkey'])

# filtrando países
selecao_paises = df1['country'].isin(paises_options)
df1 = df1.loc[selecao_paises, :]

#==========================
# layout central
#==========================
st.markdown('# Visão Cidades')
with st.container():
    st.markdown('### Top 10 cidades com mais restaurantes na base de dados')
    top_rest = top_city(df1)
    st.plotly_chart(top_rest, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('### Cidades com restaurantes com média de avaliação acima de 4')
        df_aux = media_avaliacao(df1, asc_to=False)
        st.plotly_chart(df_aux, use_container_width=True)
        
    with col2:
        st.markdown('### Cidades com restaurantes com média de avaliação abaixo de 2.5')  
        df_aux = media_avaliacao(df1, asc_to=True)
        st.plotly_chart(df_aux, use_container_width=True)

with st.container():
    st.markdown('### Top 10 cidades com mais restaurantes com tipos culinários distintos')     
    top_rest_02 = top_culin(df1)  
    st.plotly_chart(top_rest_02, use_container_width=True)
        