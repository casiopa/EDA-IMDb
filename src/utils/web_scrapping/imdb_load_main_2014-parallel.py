import pandas as pd
import numpy as np
from imdb_load_functions_parallel import read_imdb_movies
import os
import pickle

'''
title_basics = pd.read_csv('../data/imdb/title_basics.tsv', sep='\t', na_values='\\N',
                            usecols=['tconst', 'primaryTitle', 'titleType', 'startYear'])


movies_ids_2014 = title_basics[(title_basics.titleType=='movie') & (title_basics.startYear==2014.0)]
movies_ids_2014 = list(movies_ids_2014['tconst'])

with open('movies_ids_2014.pickle', 'wb') as f:
    pickle.dump(movies_ids_2014, f)
    print('Archivo pickle creado')

'''

# Aquí leo la lista de un archivo .pickle donde la he guardado previamente
# Es una lista de ids que me permite construir la url de la cada una de las páginas de película
with open('movies_ids_2014.pickle', 'rb') as f:
    movies_ids_2014 = pickle.load(f)

file_name = 'movies_df_2014.csv'

if os.path.exists(file_name):
    movies_written = pd.read_csv('movies_df_2014.csv', sep=';')

    new_movies_ids_2014 = []

    for id in movies_ids_2014:
        if id not in list(movies_written['imdb_id']):
            new_movies_ids_2014.append(id)

    read_imdb_movies(new_movies_ids_2014, file_name, 4)

else:
    read_imdb_movies(movies_ids_2014, file_name, 4)










