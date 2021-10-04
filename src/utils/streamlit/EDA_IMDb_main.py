import streamlit as st
import pandas as pd
from EDA_IMDb_functions import *



st.set_page_config(page_title='EDA - IMDb',
                   page_icon='https://www.google.com/s2/favicons?domain=www.imdb.com',
                   layout="wide")

st.sidebar.image('src/utils/streamlit/images/800px-IMDB_Logo_2016.svg.png', width=200)
st.sidebar.header('Público, crítica y taquilla en IMDb')
st.sidebar.markdown('Análisis exploratorio de datos | Películas 2014 a 2019')


menu = st.sidebar.radio(
    "",
    ("Intro", "Data", "Variables de estudio", 'Otras variables', "Relaciones entre variables", "Matrices de correlación"),
)

# Pone el radio-button en horizontal. Afecta a todos los radio button de una página.
# Por eso está puesto en este que es general a todo
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('Ana Blanco | Julio 2021 anablancodelgado@gmail.com https://casiopa.github.io/')

if menu == 'Intro':
    set_home()
elif menu == 'Data':
    set_data()
elif menu == 'Variables de estudio':
    set_variables()
elif menu == 'Otras variables':
    set_otras_variables()
elif menu == 'Relaciones entre variables':
    set_relations()
elif menu == 'Matrices de correlación':
    set_arrays()

