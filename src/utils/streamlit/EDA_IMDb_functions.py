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

    fig, ax = plt.subplots(figsize=(13,6.3))

    ax.bar(annos, n_pelis, edgecolor = "none",
        color = ['#777', '#777', '#777', '#777', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#777', '#444'])

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

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


    fig, ax = plt.subplots(figsize=(8,3.5))

    ax.bar(nmovies.index.astype(int), nmovies.values, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

    plt.xticks(nmovies.index.astype(int), fontsize=12)

    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(nmovies.index.astype(int), nmovies.values)):
        ax.text(anno, peli+10, '{0:,}'.format(peli).replace(',', '.'), va='bottom', ha = 'center', fontsize = 18, fontweight = 'regular')

    return fig


def scatter_rating_metascore(movies, size=None, color=None, title_color=''):

    fig = px.scatter(movies[movies.roi<30],
                     x="ratingImdb", y="metascore", color=color, size=size,
                     width=780, height=780, opacity=0.5,
                     color_continuous_scale=["#F5C518", "#F91949"],
                     template="plotly_dark",
                     hover_name="spanishTitle", hover_data=["ratingImdb", "metascore"]
                )
    
    if color == None:
        fig.update_traces(marker=dict(color="#F5C518"))

    fig.update_layout(coloraxis_colorbar = dict(title=title_color,
                                              ),
                      legend = dict(title = 'legend', font = {'size':14}),
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

    fig, ax = plt.subplots(figsize=(9,6.8))

    ax.barh(range(n_mvps+1,1,-1), mvps_rating.ratingImdb, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_rating.spanishTitle)):
        ax.text(.1, pos, name, va='center', ha='left', fontsize=16, fontweight='regular', color='#444')

    return fig


def barh_metascore(movies):
    plt.style.use('dark_background')

    # Preparing data
    n_mvps = 10
    mvps_metascore = movies[['spanishTitle', 'metascore']].sort_values(by='metascore', ascending=False)[:n_mvps]

    fig, ax = plt.subplots(figsize=(9,5.6))

    ax.barh(range(n_mvps+1,1,-1), mvps_metascore.metascore, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    plt.xticks(fontsize=14)

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

    fig, ax = plt.subplots(figsize=(9,6))

    ax.barh(range(n_mvps+1,1,-1), mvps_budget.budget, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,6.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_grossWorld.grossWorld, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,6))

    ax.barh(range(n_mvps+1,1,-1), mvps_profit.profit, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,5.5))

    ax.barh(range(n_mvps+1,1,-1), mvps_roi.roi, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position('none')

    plt.suptitle('-- Sin películas con un ROI > 30 --', y=.925)

    plt.xticks(fontsize=14)

    # Pintar nombre sobre las barras
    for pos, name in tuple(zip(range(n_mvps+1,1,-1), mvps_roi.spanishTitle)):
        ax.text(.5, pos, name, va='center', ha='left', fontsize=18, fontweight='regular', color='#444')

    return fig


def hist_rating(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(9,5.7))

    ax.hist(movies.ratingImdb, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    plt.xticks(range(0,11,2), fontsize=14)

    return fig


def hist_metascore(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(9,5.6))

    ax.hist(movies.metascore, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

    plt.xticks(range(0,101,25), fontsize=14)

    return fig


def hist_budget(movies):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(9,6))

    ax.hist(movies.budget, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,6.5))

    ax.hist(movies.grossWorld, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,6))

    ax.hist(movies.profit, color = '#f5c518', bins=15, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.xaxis.grid(False) 

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

    fig, ax = plt.subplots(figsize=(9,5.5))

    ax.hist(movies.roi[movies.roi<30], color = '#f5c518', bins=100, edgecolor = "none", rwidth=0.9)

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(False) 

    plt.xticks(fontsize=14)

    plt.suptitle('-- Sin películas con un ROI > 30 --', y=.91)

    return fig



def variables_rating(movies):

    st.markdown(variables_intro_rating)

    with st.beta_expander("Descriptivos Rating IMDb"):
        st.code(movies.ratingImdb.describe())

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('### Rating de usarios IMDb (2014-2019')
        st.write(hist_rating(movies))
        
    with col2:
        st.markdown('### Películas con mayor rating de usuarios en IMDb (2014-2019')
        st.write(barh_rating(movies))         
    

def variables_metascore(movies):
    st.markdown(variables_intro_metascore)

    with st.beta_expander("Descriptivos Metascore"):
        st.code(movies.metascore.describe())

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('### Metascore (2014-2019)')
        st.write(hist_metascore(movies))
    with col2:
        st.markdown('### Películas con mayor metascore en IMDb (2014-2019)')
        st.write(barh_metascore(movies))  


def variables_budget(movies):
    st.markdown(variables_intro_presupuesto)
    with st.beta_expander("Descriptivos Presupuesto"):
        st.code(movies.budget.describe())

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('### Presupuesto (2014-2019)')
        st.write(hist_budget(movies))
    with col2:  
        st.markdown('### Películas con mayor presupuesto en IMDb (2014-2019)')
        st.write(barh_budget(movies))


def variables_gross(movies):
    st.markdown(variables_intro_recaudacion)

    with st.beta_expander("Descriptivos Recaudación"):
        st.code(movies.grossWorld.describe())

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('### Recaudación (2014-2019)')
        st.write(hist_gross(movies))
    with col2:
        st.markdown('### Películas con mayor recaudación (2014-2019)')
        st.write(barh_gross(movies))


def variables_profit(movies):
    st.markdown(variables_intro_beneficio)

    with st.beta_expander("Descriptivos Beneficios"):
        st.code(movies.profit.describe())

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('### Beneficios (2014-2019)')
        st.write(hist_profit(movies))
    with col2:
        st.markdown('### Películas con mayor beneficio (2014-2019)')
        st.write(barh_profit(movies))


def variables_roi(movies):
    st.markdown(variables_intro_roi)

    with st.beta_expander("Descriptivos Retorno de la inversión (ROI)"):
        st.code(movies.roi.describe())
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Retorno de la inversión (2014-2019)')
        st.write(hist_roi(movies))
    with col2:
        st.markdown('### Películas con mayor retorno de la inversión (2014-2019)')
        st.write(barh_roi(movies))


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
            'barmode': 'stack',
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
                     template="plotly_dark", # width=1200, height=600, 
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


def ratings_counts(movies):
    ratings = pd.cut(movies.ratingImdb, [0, 2, 4, 6, 8, 10])
    ratings = ratings.value_counts().sort_index()
    ratings.index = pd.Index(['0 - 2', '2,1 - 4', '4,1 - 6', '6,1 - 8', '8,1 - 10'], name='Ratings (en rangos)')
    ratings.name = 'Número de ratings'
    return pd.DataFrame(ratings)

def metascores_counts(movies):
    metascore = pd.cut(movies.metascore, [0, 20, 40, 60, 80, 100])
    metascore = metascore.value_counts().sort_index()
    metascore.index = pd.Index(['0 - 20', '21 - 40', '41 - 60', '61 - 80', '81 - 100'], name='Metascores (en rangos)')
    metascore.name = 'Número de metascores'
    return pd.DataFrame(metascore)

def table_ratings_economicvariable(movies, economic_variable):
    movies['rating_group'] = pd.cut(movies.ratingImdb, [0, 2, 4, 6, 8, 10])
    metascores = movies.groupby('rating_group')[economic_variable].agg(['count', np.median, np.mean, np.std])
    metascores.index = pd.Index(['0 - 2', '2,1 - 4', '4,1 - 6', '6,1 - 8', '8,1 - 10'], name='Ratings IMDb (en rangos)')
    return metascores

def table_metascores_economicvariable(movies, economic_variable):
    movies['metascore_group'] = pd.cut(movies.metascore, [0, 20, 40, 60, 80, 100])
    metascores = movies.groupby('metascore_group')[economic_variable].agg(['count', np.median, np.mean, np.std])
    metascores.index = pd.Index(['0 - 20', '21 - 40', '41 - 60', '61 - 80', '81 - 100'], name='Metascores (en rangos)')
    return metascores.round(2)

def bars_ratings_counts(movies):
    ratings = pd.cut(movies.ratingImdb, [0, 2, 4, 6, 8, 10])
    ratings = ratings.value_counts().sort_index()
    ratings.index = pd.Index(['0 - 2', '2,1 - 4', '4,1 - 6', '6,1 - 8', '8,1 - 10'], name='Ratings IMDb (en rangos)')
    ratings.name = 'Número de Ratings IMDb'
    ratings = pd.DataFrame(ratings)
    
    fig = px.bar(ratings, x=ratings.index, y='Número de Ratings IMDb', text='Número de Ratings IMDb',
                 template="plotly_dark", width=700, height=480,
                )
    fig.update_traces(textposition='outside',
                      textfont={'color':"#F5C518"},
                      marker=dict(color="#F5C518"),
                     )
    fig.update_yaxes(gridcolor='#333')
    
    return fig

def bars_metascores_counts(movies):
    metascore = pd.cut(movies.metascore, [0, 20, 40, 60, 80, 100])
    metascore = metascore.value_counts().sort_index()
    metascore.index = pd.Index(['0 - 20', '21 - 40', '41 - 60', '61 - 80', '81 - 100'], name='Metascores (en rangos)')
    metascore.name = 'Número de metascores'
    metascore = pd.DataFrame(metascore)
    
    fig = px.bar(metascore, x=metascore.index, y='Número de metascores', text='Número de metascores',
                 template="plotly_dark", width=700, height=480,
                )
    fig.update_traces(textposition='outside',
                      textfont={'color':"#F5C518"},
                      marker=dict(color="#F5C518"),
                     )
    fig.update_yaxes(gridcolor='#333')
    
    return fig

def bars_rating_economicvariable(movies, economic_variable, title_y, formattext):
    movies['ratingImdb_group'] = pd.cut(movies.ratingImdb, [0, 2, 4, 6, 8, 10])
    rating_economic = pd.DataFrame(movies.groupby('ratingImdb_group')[economic_variable].median())
    rating_economic.index = ['0 - 2', '2,1 - 4', '4,1 - 6', '6,1 - 8', '8,1 - 10']
    rating_economic = rating_economic.reset_index()
    economic_variable_median = economic_variable + ' median'
    rating_economic.columns = ['rating ranges', economic_variable_median]

    fig = px.bar(rating_economic, x='rating ranges', y=economic_variable_median, text=economic_variable_median,
                 template="plotly_dark", width=700, height=480,
                )
    fig.update_traces(texttemplate=formattext,
                      textposition='outside',
                      textfont={'color':"#F5C518"},
                      marker=dict(color="#F5C518"),
                     )
    fig.update_xaxes(
        title_text = "Ratings de IMDb agrupados por rangos de 2 puntos",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = False,
    )
    fig.update_yaxes(
        title_text = title_y,
        title_font = {"size": 15},
        title_standoff = 20,
        gridcolor='#333'
    )
    
    return fig


def bars_metascore_economicvariable(movies, economic_variable, title_y, formattext):
    movies['metascore_group'] = pd.cut(movies.metascore, [0, 20, 40, 60, 80, 100])
    metascore_economic = pd.DataFrame(movies.groupby('metascore_group')[economic_variable].median())
    metascore_economic.index = ['0 - 20', '21 - 40', '41 - 60', '61 - 80', '81 - 100']
    metascore_economic = metascore_economic.reset_index()
    economic_variable_median = economic_variable + ' median'
    metascore_economic.columns = ['metascore ranges', economic_variable_median]
    
    fig = px.bar(metascore_economic, x='metascore ranges',
                         y=economic_variable_median, text=economic_variable_median,
                         template="plotly_dark", width=700, height=480,)
    
    fig.update_traces(texttemplate=formattext,
                      textposition='outside',
                      textfont={'color':"#F5C518"},
                      marker=dict(color="#F5C518"),
                     )
    fig.update_xaxes(
        title_text = "Metascores agrupados por rangos de 20 puntos",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = False,
        categoryorder='category ascending'
    )
    fig.update_yaxes(
        title_text = title_y,
        title_font = {"size": 15},
        title_standoff = 20,
        gridcolor='#333'
    )
      
    return fig   


def scatter_pointsvariable_economicvariable(movies, points_variable, economic_variable, title_points_variable, title_economic_variable):

    fig = px.scatter(movies,
                     x=points_variable, y=economic_variable, opacity=0.3,
                     template="plotly_dark",
                     hover_name="spanishTitle", hover_data=[points_variable, economic_variable],
                     #width=500, height=500,
                )
    
    fig.update_traces(marker=dict(color="#F5C518"))

    fig.update_layout(legend = dict(title = 'legend', font = {'size':14}),
                      title = dict(font = {'size':20, 'color': "#F5C518"}),
                     )

    fig.update_xaxes(
        title_text = title_points_variable,
        title_font = {"size": 15},
        title_standoff = 20,
        gridcolor='#333',
        zeroline = False,
        #type="category"
    )

    fig.update_yaxes(
        title_text = title_economic_variable,
        title_font = {"size": 15},
        title_standoff = 20,
        gridcolor='#333',
        zeroline = False
    )
    
    return fig


def strip_rating_economicvariable(movies, economic_variable, title_economic_variable):
    
    movies['ratingImdb_group'] = pd.cut(movies.ratingImdb, [0, 2, 4, 6, 8, 10])
    movies['rating_group'] = movies.rating_group.astype(str)
    rating_mapper = {'(0, 2]': '0 - 2',
                     '(2, 4]': '2,1 - 4',
                     '(4, 6]': '4,1 - 6',
                     '(6, 8]': '6,1 - 8',
                     '(8, 10]': '8,1 - 10'}
    movies['rating_group'] = movies.rating_group.replace(rating_mapper)
    
    fig = px.strip(movies,
                   x = 'rating_group', y = economic_variable,
                   template ="plotly_dark",
                   hover_name = "spanishTitle",
                   hover_data = {'rating_group': False,
                                 'ratingImdb': True,
                                 economic_variable: True},
                  )
    fig.update_traces(marker=dict(color="#F5C518",
                                  opacity = 0.3,
                                 ))
    fig.update_xaxes(categoryorder='category ascending',
                     title_text = 'Ratings de IMDb agrupados por rangos de 2 puntos'
                    )
    fig.update_yaxes(title_text = title_economic_variable,
                     gridcolor='#333',
                     zeroline = False
                    )

    return fig


def strip_metascore_economicvariable(movies, economic_variable, title_economic_variable):
    
    movies['metascore_group'] = pd.cut(movies.metascore, [0, 20, 40, 60, 80, 100])
    movies['metascore_group'] = movies.metascore_group.astype(str)
    metascore_mapper = {'(0, 20]': '0 - 20',
                        '(20, 40]': '21 - 40',
                        '(40, 60]': '41 - 60',
                        '(60, 80]': '61 - 80',
                        '(80, 100]': '81 - 100'}
    movies['metascore_group'] = movies.metascore_group.replace(metascore_mapper)
    
    fig = px.strip(movies,
                   x = 'metascore_group', y = economic_variable,
                   template ="plotly_dark",
                   hover_name = "spanishTitle",
                   hover_data = {'metascore_group': False,
                                 'metascore': True,
                                 economic_variable: True},
                  )
    fig.update_traces(marker=dict(color="#F5C518",
                                  opacity = 0.3,
                                 ))
    fig.update_xaxes(categoryorder='category ascending',
                     title_text = 'Metascores agrupados por rangos de 20 puntos'
                    )
    fig.update_yaxes(title_text = title_economic_variable,
                     gridcolor='#333',
                     zeroline = False
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
    #st.header('Relaciones entre valoraciones de público y crítica, y la recaudación\n Películas en IMDb 2014 - 1019')
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
    st.write(intro_herramientas_fuentes, unsafe_allow_html=True)


def set_data():
    movies = load_csv(path)
    rates = pd.read_csv(path_rates)

    st.title('Data')
    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### Nº de películas en IMDb')
        st.markdown('117.482 páginas de películas (2014-2020) escrapeadas del portal IMDb')
        st.markdown(' ')
        st.write(bars_nmovies_imdb())

    with col2:
        st.markdown('### Nº de películas de IMDb filtradas')
        st.markdown('Datos resultantes tras filtrar las películas con rating, metascore, presupuesto o recaudación. 1.553 películas')
        st.write(bars_nmovies(movies))

    st.markdown('### DataFrame `movies`')
    st.markdown('DataFrame final preparado para el estudio tras filtrar las películas con rating, metascore, presupuesto o recaudación. 1.553 películas.')
    st.markdown('1.553 entries  |  24 columns')
    st.write(movies)

    st.markdown('### DataFrame `rates`')
    st.markdown('DataFrame generado con información de la OCDE y otras fuetes con la tasa de cambio para las países y años del dataset.')
    st.markdown('4.123 entries  |  8 columns')
    st.write(rates)


def set_variables():
    movies = load_csv(path) 
    st.title('Variables de estudio - Valoraciones y recaudación')
 
    menu_variables= st.radio(
        "",
        ("Intro variables", "Rating","Metascore", "Presupuesto", "Recaudación", "Beneficios", "ROI"),
    )

    if menu_variables == "Intro variables":
        st.markdown(variables_intro)
    elif menu_variables == "Rating":
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
        st.markdown('### Número de películas por género')
        st.markdown('La distribuicón por géneros de las palículas es similar en los años de estudio, con con tres 4 géneros que representan la gran mayoría de las películas: Acción, Drama, Comedia  y Biografías/Documentales.')
        st.write(stack_bar_genres(movies))
    elif menu_otras_variables == "Países":
        st.markdown('### Número de películas por país de origen')
        st.markdown('Estados Unidos es el país con mayor número de producciones con 892 películas, seguido de Reino Unido con 185 y en tercer lugar se encuentra Francia con 98 películas producidas. También es de interés el mercado canadiense con 56 producciones. Finalmente, España se encuentra representada por 26 películas.')
        st.write(map_countries(movies))



def set_relations():
    movies = load_csv(path) 
    st.title('Relaciones entre variables')

    menu_relations= st.radio(
        "",
        ("Rating/Metascore", "R/M/Presupuesto", "R/M/Presupuesto/Beneficio", "R/M/Presupuesto/ROI"),
    )

    if menu_relations == "Rating/Metascore":

        st.markdown('### Relación entre Rating y Metascore')
        st.write(scatter_rating_metascore(movies))

        menu_relations_ranking_metascore = st.radio(
        "",
            ("Rating", "Metascore"),
        )   

        if menu_relations_ranking_metascore == "Rating":
            st.markdown('### Cantidad de Ratings IMDb agrupados por rangos de 2 puntos')    
            st.write(ratings_counts(movies))
            st.write(bars_ratings_counts(movies))
        elif menu_relations_ranking_metascore == "Metascore":
            st.markdown('### Cantidad de Metascores agrupados por rangos de 20 puntos')
            st.write(metascores_counts(movies))
            st.write(bars_metascores_counts(movies))
        
    elif menu_relations == "R/M/Presupuesto":

        st.markdown('### Relación entre Rating, Metascore y Presupuesto (tamaño)')
        st.write(scatter_rating_metascore(movies, size='budget'))

        menu_relations_budget = st.radio(
        "",
            ("Relación entre Rating y Presupuesto", "Relación entre Metascore y Presupuesto"),
        )   

        if menu_relations_budget == "Relación entre Rating y Presupuesto":
            st.write(scatter_pointsvariable_economicvariable(movies, 'ratingImdb', 'budget', title_points_variable='Rating de IMDb (1-10)', title_economic_variable='Presupuesto ($)'))
            st.markdown('### Presupuesto por rangos de Ratings IMDb')
            st.write(table_ratings_economicvariable(movies, 'budget'))
            st.write(strip_rating_economicvariable(movies, economic_variable='budget', title_economic_variable='Presupuesto ($)'))
        elif menu_relations_budget == "Relación entre Metascore y Presupuesto":
            st.write(scatter_pointsvariable_economicvariable(movies, 'metascore', 'budget', title_points_variable='Metascore (1-100)', title_economic_variable='Presupuesto ($)'))
            st.markdown('### Presupuesto por rangos de Metascore')
            st.write(table_metascores_economicvariable(movies, 'budget'))
            st.write(strip_metascore_economicvariable(movies, economic_variable='budget', title_economic_variable='Presupuesto ($)'))
        
        

    elif menu_relations == "R/M/Presupuesto/Beneficio":

        st.markdown('### Relación entre Rating, Metascore, Presupuesto (tamaño) y Beneficio (color)')
        st.write(scatter_rating_metascore(movies, size='budget', color='profit', title_color = 'Beneficio'))

        menu_relations_profit = st.radio(
        "",
            ("Relación entre Rating y Beneficio", "Relación entre Metascore y Beneficio"),
        )   

        if menu_relations_profit == "Relación entre Rating y Beneficio":
            st.write(scatter_pointsvariable_economicvariable(movies, 'ratingImdb', 'profit', title_points_variable='Rating de IMDb (1-10)', title_economic_variable='Beneficio ($)'))
            st.markdown('### Beneficio por rangos de Ratings IMDb')
            st.write(table_ratings_economicvariable(movies, 'profit'))
            st.write(strip_rating_economicvariable(movies, economic_variable='profit', title_economic_variable='Beneficio ($)'))
        elif menu_relations_profit == "Relación entre Metascore y Beneficio":
            st.write(scatter_pointsvariable_economicvariable(movies, 'metascore', 'profit', title_points_variable='Metascore (1-100)', title_economic_variable='Beneficio ($)'))
            st.markdown('### Beneficio por rangos de Metascore')
            st.write(table_metascores_economicvariable(movies, 'profit'))
            st.write(strip_metascore_economicvariable(movies, economic_variable='profit', title_economic_variable='Beneficio ($)'))

        

    elif menu_relations == "R/M/Presupuesto/ROI":

        st.markdown('### Relación entre Rating, Metascore, Presupuesto (tamaño) y ROI (color)')
        st.write(scatter_rating_metascore(movies, size='budget', color='roi', title_color = 'ROI'))

        menu_relations_roi = st.radio(
        "",
            ("Relación entre Rating y ROI", "Relación entre Metascore y ROI"),
        )   

        if menu_relations_roi == "Relación entre Rating y ROI":
            st.write(scatter_pointsvariable_economicvariable(movies[movies.roi<30], 'ratingImdb', 'roi', title_points_variable='Rating de IMDb (1-10)', title_economic_variable='ROI'))
            st.markdown('### ROI por rangos de Ratings IMDb')
            st.write(table_ratings_economicvariable(movies, 'roi'))
            st.write(strip_rating_economicvariable(movies[movies.roi<30], economic_variable='roi', title_economic_variable='ROI'))
        elif menu_relations_roi == "Relación entre Metascore y ROI":
            st.write(scatter_pointsvariable_economicvariable(movies[movies.roi<30], 'metascore', 'roi', title_points_variable='Metascore (1-100)', title_economic_variable='ROI'))
            st.markdown('### ROI por rangos de Metascore')
            st.write(table_metascores_economicvariable(movies, 'roi'))
            st.write(strip_metascore_economicvariable(movies[movies.roi<30], economic_variable='roi', title_economic_variable='ROI'))

        



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

