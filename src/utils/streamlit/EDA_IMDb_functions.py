import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly import tools
from EDA_IMDb_variables import *



#@st.cache
def load_csv(path):
    data = pd.read_csv(path, sep=';')
    return data


def bars_nmovies_imdb():
    # Número de pelis por año en IMDb
    n_pelis = [12218, 13148, 14105, 14791, 15862, 16412, 17609, 17967, 17819, 17181, 14632, 11842]

    annos = np.arange(2010,2022)

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(13,6))

    ax.bar(annos, n_pelis, edgecolor = "none",
        color = ['#777', '#777', '#777', '#777', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#777', '#444'])

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

    plt.title('Nº de películas en IMDb', fontdict={'fontname': 'Roboto', 'fontsize': 22, 'fontweight': 'bold', 'color': '#f5c518'}, pad=35)

    annos_xticks = annos.astype(str)
    annos_xticks[11] = 'jun\n2021'
    plt.xticks(annos, labels=annos_xticks, fontsize=12)

    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(annos, n_pelis)):
        ax.text(anno, peli+200, '{0:,}'.format(peli).replace(',', '.'), va='bottom', ha = 'center', fontsize = 14, fontweight = 'regular');
    
    return fig


def bars_nmovies(movies):
    plt.style.use('dark_background')

    #prepare data
    nmovies = movies.groupby('year')['year'].count()


    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(nmovies.index.astype(int), nmovies.values, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

    #plt.title('Nº de películas de IMDb seleccionadas', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=45)


    plt.xticks(nmovies.index.astype(int), fontsize=12)

    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(nmovies.index.astype(int), nmovies.values)):
        ax.text(anno, peli+10, '{0:,}'.format(peli).replace(',', '.'), va='bottom', ha = 'center', fontsize = 18, fontweight = 'regular')

    return fig


def scatter_rating_metascore(movies, size):
    movies['year'] = movies['year'].astype(int).astype('category')

    fig = px.scatter(movies[movies.roi<30],
                 x="ratingImdb", y="metascore", color="year", size=size,
                 #title="Relación entre Rating y Metascore",
                 width=780, height=780,
                 color_discrete_map={ # replaces default color mapping by value
                     2014: "#F52E18", 2015: "#F52E18", 2016: "#F55418", 2017: "#F57A18", 2018: "#F59F18", 2019: "#F5C518", 
                 },
                 template="plotly_dark",
                 hover_name="spanishTitle", hover_data=["ratingImdb", "metascore"]
                )

    fig.update_layout(
        legend = dict(title = '', font = {'size':14}),
        title = dict(font = {'size':20, 'color': "#F5C518"}),
    )

    fig.update_xaxes(
        title_text = "Rating de IMDb (1-10)",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = False,
        showline = False,
        showticklabels = False,
        zeroline = False
    )

    fig.update_yaxes(
        title_text = "Metascore (1-100)",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = False,
        showline = False,
        showticklabels = False,
        zeroline = False
    )


    gris = '#999'


    fig.add_shape( # línea horizontal
        type="line", line_color=gris, line_width=1, opacity=1,
        x0=0, x1=10, xref="x", y0=50, y1=50, yref="y"
    )

    fig.add_annotation( # texto línea horizontal  
        text="Suspenso Metascore", x=1.3, y=48, showarrow=False, font = {'color': gris, 'size':14}
    )

    fig.add_shape( # línea vertical
        type="line", line_color=gris, line_width=1, opacity=1,
        x0=5, x1=5, xref="x", y0=0, y1=100, yref="y"
    )

    fig.add_annotation( # texto línea vertical  
        text="Suspenso Rating IMDb", x=3.5, y=-2, showarrow=False, font = {'color': gris, 'size':14}
    )

    return fig


def barh_rating(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_rating = movies[['spanishTitle', 'ratingImdb']].sort_values(by='ratingImdb', ascending=False)[:n_mvps]

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_rating.ratingImdb, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)
    #plt.title('Películas con mayor rating de usuarios en IMDd', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=15)


    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_rating.spanishTitle)):
        ax.text(.1, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')

    return fig


def barh_metascore(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_metascore = movies[['spanishTitle', 'metascore']].sort_values(by='metascore', ascending=False)[:n_mvps]

    fig, ax = plt.subplots(figsize=(10,7))

    ax.barh(range(n_mvps+1,1,-1), mvps_metascore.metascore, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)
    #plt.title('Películas con mayor metascore', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=15)


    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_metascore.spanishTitle)):
        ax.text(1, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')

    return fig


def barh_budget(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_budget = movies[['spanishTitle', 'budget']].sort_values(by='budget', ascending=False)[:n_mvps]
    mvps_budget

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_budget.budget, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

    #plt.title('Películas con mayor presupuesto', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=15)
    plt.xlabel('Millones de dólares', labelpad=15)

    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels = [int(item)*10 for item in labels]

    ax.set_xticklabels(labels)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_budget.spanishTitle)):
        ax.text(5000000, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')
    
    return fig


def barh_gross(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_grossWorld = movies[['spanishTitle', 'grossWorld']].sort_values(by='grossWorld', ascending=False)[:n_mvps]

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_grossWorld.grossWorld, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

    #plt.title('Películas con mayor recaudación mundial', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=15)
    plt.xlabel('Millones de dólares', labelpad=15)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels[1]=0
    labels = [int(item)*100 for item in labels]
    labels = ['{:,.2f}'.format(item).replace(".", "").replace(",", ".")[:-2] for item in labels]

    ax.set_xticklabels(labels)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_grossWorld.spanishTitle)):
        ax.text(20000000, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')

    return fig


def barh_profit(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_profit = movies[['spanishTitle', 'profit']].sort_values(by='profit', ascending=False)[:n_mvps]

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_profit.profit, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

    #plt.title('Películas con mayor beneficio', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=15)
    plt.xlabel('Millones de dólares', labelpad=15)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels[1]=0
    labels = [int(item)*100 for item in labels]
    labels = ['{:,.2f}'.format(item).replace(".", "").replace(",", ".")[:-2] for item in labels]

    ax.set_xticklabels(labels)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_profit.spanishTitle)):
        ax.text(20000000, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')

    return fig


def barh_roi(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_roi = movies[(movies.roi<30)][['spanishTitle', 'roi']].sort_values(by='roi', ascending=False)[:n_mvps]
    mvps_roi

    fig, ax = plt.subplots(figsize=(10,7.42))

    ax.barh(range(n_mvps+1,1,-1), mvps_roi.roi, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    #plt.title('Películas con mayor Retorno de la inversión (ROI)', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=40)
    plt.suptitle('-- Sin películas con un ROI > 30 --', y=.925)

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_roi.spanishTitle)):
        ax.text(.5, pos, name, va='center', ha='left', fontsize=18, fontweight='regular', color='#444')

    return fig


def hist_rating(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7))

    ax.hist(movies.ratingImdb, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    #plt.title('Rating de usuarios IMDb', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)

    plt.xticks(range(0,11,2), fontsize=14)

    return fig


def hist_metascore(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7))

    ax.hist(movies.metascore, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    #plt.title('Metascore', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)
    plt.xticks(range(0,101,25), fontsize=14)

    return fig


def hist_budget(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.hist(movies.budget, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    #plt.title('Presupuesto', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)
    plt.xlabel('Millones de dólares', labelpad=15)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels[1]=0
    labels = [int(item)*10 for item in labels]
    ax.set_xticklabels(labels)

    plt.xticks(fontsize=14)

    return fig


def hist_gross(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.hist(movies.grossWorld, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    #plt.title('Recaudación mundial', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)
    plt.xlabel('Millones de dólares', labelpad=15)
    plt.xticks(fontsize=14)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels[1]=0
    labels = [int(item)*100 for item in labels]
    labels = ['{:,.2f}'.format(item).replace(".", "").replace(",", ".")[:-2] for item in labels]
    ax.set_xticklabels(labels)

    return fig
    

def hist_profit(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.hist(movies.profit, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    #plt.title('Beneficio', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)
    plt.xlabel('Millones de dólares', labelpad=15)
    plt.xticks(fontsize=14)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace('.', '') for item in ax.get_xticklabels()]
    labels[0]=0
    labels[1]=0
    labels = [int(item)*100 for item in labels]
    labels = ['{:,.2f}'.format(item).replace(".", "").replace(",", ".")[:-2] for item in labels]
    ax.set_xticklabels(labels)

    return fig


def hist_roi(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(10,7.5))

    ax.hist(movies.roi[movies.roi<30], color = '#f5c518', bins=100, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

    plt.xticks(fontsize=14)

    #plt.title('Rentabilidad (ROI)', fontdict={'fontname': 'Roboto', 'fontsize': 20, 'fontweight': 'bold', 'color': '#f5c518'}, pad=20)
    plt.suptitle('-- Sin películas con un ROI > 30 --', y=.91)

    return fig



def variables_rating(movies):
    with st.beta_expander("Descriptivos Rating IMDb"):
        st.code(movies.ratingImdb.describe())

    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor rating de usuarios en IMDb')
        st.write(barh_rating(movies))

    with col2:
        st.markdown('### Rating de usarios IMDb')
        st.write(hist_rating(movies)) 
    

def variables_metascore(movies):
    with st.beta_expander("Descriptivos Metascore"):
        st.code(movies.metascore.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor metascore en IMDb')
        st.write(barh_metascore(movies))
    with col2:
        st.markdown('### Metascore')
        st.write(hist_metascore(movies))  


def variables_budget(movies):
    with st.beta_expander("Descriptivos Presupuesto"):
        st.code(movies.budget.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor presupuesto en IMDb')
        st.write(barh_budget(movies))
    with col2:
        st.markdown('### Presupuesto')
        st.write(hist_budget(movies))  


def variables_gross(movies):
    with st.beta_expander("Descriptivos Recaudación"):
        st.code(movies.grossWorld.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor recaudación')
        st.write(barh_gross(movies))
    with col2:
        st.markdown('### Recaudación')
        st.write(hist_gross(movies))  


def variables_profit(movies):
    with st.beta_expander("Descriptivos Beneficios"):
        st.code(movies.profit.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor beneficio')
        st.write(barh_profit(movies))
    with col2:
        st.markdown('### Beneficios')
        st.write(hist_profit(movies))  


def variables_roi(movies):
    with st.beta_expander("Descriptivos Retorno de la inversión (ROI)"):
        st.code(movies.roi.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Películas con mayor retorno de la inversión')
        st.write(barh_roi(movies))
    with col2:
        st.markdown('### Retorno de la inversión')
        st.write(hist_roi(movies))  


def first_elem_csv(csv):
    if str(csv) == 'nan':
        return np.nan
    else:
        return csv.split(',')[0]


### Agrupación de los géneros en 6 categorías
def grouppingGenres(genre):
    if (genre == 'Biography') | (genre == 'Documentary'):
        return 'Bio-Documentary'
    elif genre == 'Crime':
        return 'Thriller'
    elif genre == 'Fantasy':
        return 'Adventure'
    elif genre == 'Family':
        return 'Adventure'
    else:
        return genre


def primaryGenre(movies):

    movies['primaryGenre'] = movies['genres'].apply(first_elem_csv)    
    movies['primaryGenre'] = movies['primaryGenre'].apply(grouppingGenres)

    return movies


def heatmap_6x6(corr_6x6):
    fig = ff.create_annotated_heatmap(corr_6x6.round(2).to_numpy().tolist(),
                x=['Rating de IMDb', 'Metascore', 'Presupuesto', 'Recaudación', 'Beneficio', 'ROI'],
                y=['Rating de IMDb', 'Metascore', 'Presupuesto', 'Recaudación', 'Beneficio', 'ROI'],
                colorscale=[[0, "black"], [1, '#f5c518']],
                font_colors = ['white', 'black'],
                showscale=True,
                zmin=0, zmax=1,
               )

    fig.update_layout(width=800, height=700,  template="plotly_dark")

    fig.update_yaxes(
        autorange="reversed"
    )    

    # Make text size bigger
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 14

    return fig


def heatmap_2x4(corr_2x4):
    fig = ff.create_annotated_heatmap(corr_2x4.round(2).to_numpy().tolist(),
                x=['Presupuesto', 'Recaudación', 'Beneficio', 'ROI'],
                y=['Rating de IMDb', 'Metascore'],
                colorscale=[[0, "black"], [1, '#f5c518']],
                font_colors = ['white'],
                showscale=True,
                zmin=0, zmax=1,
               )

    fig.update_layout(width=800, height=500,  template="plotly_dark"
                    )

    fig.update_xaxes(
        title_text = "Recaudación",
        title_font = {"size": 15},
        title_standoff = 20,
    )

    fig.update_yaxes(
        title_text = "Valoraciones",
        title_font = {"size": 15},
        title_standoff = 20,
        autorange="reversed"
    )    

    # Make text size bigger
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 14

    return fig


def stack_bar_genres(movies):

    # Preparar el dataset
    movies = primaryGenre(movies)


    # Crear la tabla adecuada para el bar stick de plotly
    genres_by_year = movies.groupby(['year','primaryGenre'])[['primaryGenre']].count().unstack().T
    genres_by_year.index = genres_by_year.index.droplevel()
    genres_by_year.columns = genres_by_year.columns.astype(int)


    # Ordenar el df por la nueva columna total
    genres_by_year['TOTAL'] = genres_by_year.sum(axis=1)
    genres_by_year.sort_values(by=['TOTAL'], inplace=True, ascending=False)
    genres_by_year = genres_by_year[genres_by_year['TOTAL']>1]

    x = genres_by_year.index

    trace1 = {
    'x': x,
    'y': genres_by_year[2014],
    'name': '2014',
    'type': 'bar',
    'marker': {'color': '#F52E18'}
    }


    trace2 = {
        'x': x,
        'y': genres_by_year[2015],
        'name': '2015',
        'type': 'bar',
        'marker': {'color': '#F52E18'}
    }


    trace3 = {
        'x': x,
        'y': genres_by_year[2016],
        'name': '2016',
        'type': 'bar',
        'marker': {'color': '#F55418'}
    }

    trace4 = {
        'x': x,
        'y': genres_by_year[2017],
        'name': '2017',
        'type': 'bar',
        'marker': {'color': '#F57A18'}
        
    }

    trace5 = {
        'x': x,
        'y': genres_by_year[2018],
        'name': '2018',
        'type': 'bar',
        'marker': {'color': '#F59F18'}
    }

    trace6 = {
        'x': x,
        'y': genres_by_year[2019],
        'name': '2019',
        'type': 'bar',
        'marker': {'color': '#F5C518'}   ## Colores 2019-2014: '#F5184F', '#F52E18', '#F55418', '#F57A18', '#F59F18', '#F5C518'
    }

    data = [trace6, trace5, trace4, trace3, trace2, trace1]

    layout = {'xaxis': {'title': ''},
            'font': {'family':"Roboto", 'size':16},
            'title_font_family': 'Roboto',
            #'title_font_color':'#F5C518',
            'height': 600,
            'width': 1200,
            'barmode': 'stack',
            'title': 'Número de películas por género',
            'template' : "plotly_dark",
            'plot_bgcolor':'rgba(50,50,50,1)'
            }

    fig = go.Figure(data = data, layout = layout)
    return fig



def map_countries(movies):

    # Selección del primer país de la lista de países y creación de tabla counts de países
    movies['primaryCountry'] = movies['countries'].apply(first_elem_csv)
    countries_count = movies.groupby('primaryCountry')[['primaryCountry']].count()
    countries_count.rename(columns={'primaryCountry': 'countryCounts'}, inplace=True)
    countries_count.reset_index(inplace=True)

    fig = px.scatter_geo(countries_count, locations="primaryCountry",
                     hover_name="primaryCountry", size="countryCounts", text = 'countryCounts',
                     projection="equirectangular", locationmode = 'country names',
                     width=1200, height=600, template="plotly_dark",
                    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                 plot_bgcolor='rgba(0,0,0,0)',
                 paper_bgcolor='rgba(0,0,0,0)')


    fig.update_traces(marker = dict(color = '#f5c518',
                                    line_width=0,
                                    sizeref=.1,
                                sizemin=5),
                    mode = 'markers+text',
                    textfont = dict(size=10)
                    )
    return fig


def set_home():
    md_parasite = 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UY720_.jpg'
    md_boyhood = 'https://m.media-amazon.com/images/M/MV5BMTYzNDc2MDc0N15BMl5BanBnXkFtZTgwOTcwMDQ5MTE@._V1_FMjpg_UX1000_.jpg'
    md_endgame = 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UY720_.jpg'
    md_interstellar = 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UY720_.jpg'
    md_showman = 'https://m.media-amazon.com/images/M/MV5BYjQ0ZWJkYjMtYjJmYS00MjJiLTg3NTYtMmIzN2E2Y2YwZmUyXkEyXkFqcGdeQXVyNjk5NDA3OTk@._V1_FMjpg_UY720_.jpg'
    md_split = 'https://m.media-amazon.com/images/M/MV5BZTJiNGM2NjItNDRiYy00ZjY0LTgwNTItZDBmZGRlODQ4YThkL2ltYWdlXkEyXkFqcGdeQXVyMjY5ODI4NDk@._V1_FMjpg_UY720_.jpg'
    md_sw_despertar = 'https://m.media-amazon.com/images/M/MV5BOTAzODEzNDAzMl5BMl5BanBnXkFtZTgwMDU1MTgzNzE@._V1_FMjpg_UY720_.jpg'
    md_lalaland = 'https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_FMjpg_UY720_.jpg'
    st.header('Relaciones entre valoraciones de público y crítica, y la recaudación\n Películas en IMDb 2014 - 1019')
    #st.subheader('Relaciones entre valoraciones de público y crítica, y la recaudación')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.beta_columns(8)

    with col1:
        st.image(md_parasite, use_column_width='always')
    with col2:
        st.image(md_endgame, use_column_width='always')
    with col3:
        st.image(md_showman, use_column_width='always')
    with col4:
        st.image(md_interstellar, use_column_width='always')
    with col5:
        st.image(md_boyhood, use_column_width='always')
    with col6:
        st.image(md_split, use_column_width='always')
    with col7:
        st.image(md_sw_despertar, use_column_width='always')
    with col8:
        st.image(md_lalaland, use_column_width='always')

    st.write(intro, unsafe_allow_html=True)

    col1, col2 = st.beta_columns([2,1])
    with col1:
        st.image('images/Relacion_Rating_Metascore.png')

    st.markdown('''
    Si relacionamos las valoraciones con la información económica de las películas podemos observar que no guarda gran relación con el presupuesto, pues encontramos películas de alto presupuesto suspensas en las calificaciones. Sin embargo si relacionamos las valoraciones con el beneficio observamos que una tendencia de mayor puntuaciones a mayor beneficio. La variable beneficio conlleva implícitamente dos conceptos: éxito en taquilla y alto presupuesto. Este tipo de película tiende a ser bien valorado por los usuarios de IMDb.
    ''')

    col1, col2 = st.beta_columns(2)
    with col1:
        st.image('images/Relacion_Rating_Metascore_Budget.png')
    with col2:
        st.image('images/Relacion_Rating_Metascore_Profit.png')

    st.markdown('''Si bien la correlación entre las valoraciones y los datos económicos de las películas es débil. Pero sí es cierto que la tendencia es más fuerte para el rating de usuarios que para la valoración de los críticos (Metascore).''')

    col1, col2 = st.beta_columns([2,1])
    with col1:
        st.image('images/corr_2x4.png')

    st.markdown('''
    Ciertos subgrupos de la muestra de película tienen una mayor correlación, como los géneros del tipo de acción, thriller y horror, y a nivel de países también mejora la correlación cuando nos centramos en EEUU (país de origen del portal IMDb.
    ''')

    col1, col2 = st.beta_columns(2)
    with col1:
        st.image('images/corr_2x4_paises_eeuu.png')
    with col2:
        st.image('images/corr_2x4_genero_action.png')

    st.write(intro_herramientas_fuentes, unsafe_allow_html=True)


def set_data():
    movies = load_csv(path)
    rates = pd.read_csv(path_rates)

    st.title('Data')
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Nº de películas en IMDb')
        st.markdown('117.482 páginas de películas escrapeadas (2014-2020)')
        st.write(bars_nmovies_imdb())


    with col2:
        st.markdown('### Nº de películas de IMDb filtradas')
        st.markdown('1.553 películas')
        st.write(bars_nmovies(movies))

    st.markdown('### DataFrame `movies`')
    st.markdown('1553 entries  |  24 columns')
    st.write(movies)

    st.markdown('### DataFrame `rates`')
    st.markdown('4123 entries  |  8 columns')
    st.write(rates)



def set_variables():
    movies = load_csv(path) 
    st.title('Variables de estudio - Valoraciones y recaudación')

    menu_variables= st.radio(
        "",
        ("Rating","Metascore", "Presupuesto", "Recaudación", "Beneficios", "ROI"),
    )

    if menu_variables == "Rating":
        variables_rating(movies)
    elif menu_variables == "Metascore":
        variables_metascore(movies)
    elif menu_variables == "Presupuesto":
        variables_budget(movies)
    elif menu_variables == "Recaudación":
        variables_gross(movies)
    elif menu_variables == "Beneficios":
        variables_profit(movies)
    elif menu_variables == "ROI":
        variables_roi(movies)



def set_otras_variables():
    movies = load_csv(path) 
    st.title('Otras variables')

    menu_otras_variables = st.radio(
        "",
        ("Géneros", "Países"),
    )

    if menu_otras_variables == "Géneros":
        st.write(stack_bar_genres(movies))
    elif menu_otras_variables == "Países":
        st.write(map_countries(movies))



def set_relations():
    movies = load_csv(path) 
    st.title('Relaciones entre variables')

    menu_relations= st.radio(
        "",
        ("Rating/Metascore", "Rating/Metascore/Presupuesto", "Rating/Metascore/Beneficio"),
    )

    if menu_relations == "Rating/Metascore":
        st.write(scatter_rating_metascore(movies, None))
    elif menu_relations == "Rating/Metascore/Presupuesto":
        st.write(scatter_rating_metascore(movies, 'budget'))
    elif menu_relations == "Rating/Metascore/Beneficio":
        st.write(scatter_rating_metascore(movies[(movies.profit>=0)], 'profit'))




def set_arrays():
    movies = load_csv(path) 
    st.title('Matrices de correlación')

    corr_6x6 = movies[movies.roi<30][['ratingImdb', 'metascore', 'budget', 'grossWorld', 'profit', 'roi']].corr()
    corr_2x4 = corr_6x6.loc['ratingImdb': 'metascore', 'budget':'roi']

    menu_arrays= st.radio(
        "",
        ("6x6", "2x4", "Géneros", "Países"),
    )

    if menu_arrays == "6x6":
        st.write(heatmap_6x6(corr_6x6))
    elif menu_arrays == "2x4":
        st.write(heatmap_2x4(corr_2x4))
    elif menu_arrays == 'Géneros':

        menu_genre = st.radio(
            "",
            ('Action', 'Drama', 'Comedy', 'Bio-Documentary', 'Adventure', 'Thriller', 'Horror', 'Animation')
        )
        
        movies = primaryGenre(movies)
        corr_genre = movies[(movies.roi<30) & (movies.primaryGenre==menu_genre)][['ratingImdb', 'metascore', 'budget', 'grossWorld', 'profit', 'roi']].corr().loc['ratingImdb': 'metascore', 'budget':'roi']
        st.write(heatmap_2x4(corr_genre))

        st.write('### Descriptivos para el Rating de usuarios según los géneros')
        movies['primaryGenre'] = movies['primaryGenre'].apply(grouppingGenres)
        rating_genres = movies.groupby('primaryGenre').ratingImdb.describe().T[['Action', 'Adventure', 'Animation', 'Bio-Documentary',
                                        'Comedy', 'Drama', 'Horror', 'Thriller']]
        st.table(rating_genres)

        st.write('### Descriptivos para el Metascore según los géneros')
        metascore_genres = movies.groupby('primaryGenre').metascore.describe().T[['Action', 'Adventure', 'Animation', 'Bio-Documentary',
                                        'Comedy', 'Drama', 'Horror', 'Thriller']]
        st.table(metascore_genres)

    elif menu_arrays == 'Países':
        
        menu_country = st.radio(
            "",
            ('United States', 'United Kingdom', 'France', 'Canada', 'China', 'Spain')
        )

        movies['primaryCountry'] = movies['countries'].apply(first_elem_csv)
        corr_country = movies[(movies.roi<30) & (movies.primaryCountry==menu_country)][['ratingImdb', 'metascore', 'budget', 'grossWorld', 'profit', 'roi']].corr().loc['ratingImdb': 'metascore', 'budget':'roi']
        st.write(heatmap_2x4(corr_country))

        st.write('### Descriptivos para el Rating de usuarios según los países de origen')
        rating_countries = movies.groupby('primaryCountry').ratingImdb.describe().T[['United States', 'United Kingdom', 'France', 'Canada', 'China', 'Spain']]
        st.table(rating_countries)

        st.write('### Descriptivos para el Metascore según los países de origen')
        metascore_countries = movies.groupby('primaryCountry').metascore.describe().T[['United States', 'United Kingdom', 'France', 'Canada', 'China', 'Spain']]
        st.table(metascore_countries)
