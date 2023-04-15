# Libries
import pandas as pd
import streamlit as st
import plotly.express as px

import folium 
import numpy as np
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Países', layout='wide' )
#==========================
# import dataset
#==========================
df = pd.read_csv('dataset/zomato.csv')

#==========================
# listas (Países, cores)
#==========================

# Países
COUNTRIES = {
    1 : "India",
    14 : "Australia",
    30 : "Brazil",
    37 : "Canada",
    94 : "Indonesia",
    148 : "New Zeland",
    162 : "Philippines",
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

def rename_colors(df):
    """ Essa função renomeia a coluna cor

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
    df['country'] = df['country'].apply( lambda x: COUNTRIES[x])
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
                            'Country Code': 'country', 'Locality Verbose': 'locality_details', 'Average Cost for two' : 'custo_medio_p_dois',
                            'Has Table booking': 'reserva_mesa','Has Online delivery' : 'entrega_online' , 'Is delivering now' : 'entregando_agora' ,
                            'Switch to order menu' : 'mudar_menu_pedidos' , 'Price range' : 'faixa_preco' , 'Aggregate rating' : 'avaliacao_detalhada', 
                            'Rating color' : 'cor' , 'Rating text' : 'avaliacao' , 'Votes' : 'votos'})
    
    return df_rename


def media_ava(df1):    
    """ Essa função calcula a média de avaliação por país.

        Input: dataframe
        Output: gráfico em barras 
        
    """
    df1 = ( np.round(df1
            .loc[:, ['avaliacao_detalhada', 'country']]
            .groupby('country')
            .mean()
            .sort_values('avaliacao_detalhada', ascending=False)
            .reset_index().head(6), 2) )
        
    df1.columns = ['Países', 'Avaliação']
    fig = px.bar(df1, x='Países', y='Avaliação', text_auto=True)
        
    return fig

def qtd_rest(df1): 
    """ Essa função calcula a quantidade de restaurantes por país.
    

        Input: dataframe 
        Output: gráfico em barras 
        
    """
    df1 = ( df1.loc[:, ['restaurant_ID', 'country']]
               .groupby('country')
               .count()
               .sort_values('restaurant_ID', ascending=False)
               .reset_index().head(6) )
    
    df1.columns = ['Países', 'Quantidade de Restaurantes']
    fig = px.bar(df1, x='Países', y='Quantidade de Restaurantes', text_auto=True)
    
    return fig

def qtd_city(df1):
    """ Essa função calcula a quantidade de cidades resgistradas por país.

    Input: dataframe
    Output: gráfico em barras
    """
         
    df1 = ( df1.loc[:,['City', 'country']]
               .groupby('country')
               .count()
               .sort_values('City', ascending=False)
               .reset_index().head(6) )
        
    df1.columns = ['Países', 'Cidades']
    fig = px.bar(df1, x='Países', y='Cidades', text_auto=True)
    
    return fig

def media_prato(df1):   
    """ Essa função calcula a média de custo de um prato para duas pessoas.

        Input: dataframe
        Output: gráfico em barras
        
    """
    df1 = ( np.round(df1
              .loc[:, ['custo_medio_p_dois', 'country']]
              .groupby('country')
              .mean()
              .sort_values('custo_medio_p_dois', ascending=False)
              .reset_index().head(6), 2) )
        
    df1.columns = ['Países','Custo médio']
    fig = px.bar(df1, x='Países', y='Custo médio', text_auto=True)
    
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
st.sidebar.markdown('# Filtros')

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

#==========================
# layout central
#==========================

st.markdown('# Visão Países')   

with st.container():
     st.markdown('### Quantidade de Restaurantes Registrados por País ')
     num_rest = qtd_rest(df1)
     st.plotly_chart(num_rest, use_container_width=True)
    
with st.container():    
     st.markdown('### Quantidade de Cidades Registrados por País')
     num_city = qtd_city(df1)
     st.plotly_chart(num_city, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2, gap='large')    
    with col1:
        st.markdown('### Média de Avaliação feita por país')
        media_avaliacao = media_ava(df1)
        st.plotly_chart(media_avaliacao, use_container_width=True)
        
    with col2:
        st.markdown('### Média de Preço de um prato para duas pessoas por País')
        media = media_prato(df1)
        st.plotly_chart(media, use_container_width=True)
    
    
    