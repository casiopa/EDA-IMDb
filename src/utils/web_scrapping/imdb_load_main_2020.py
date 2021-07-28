import pandas as pd
import numpy as np
from imdb_load_functions import read_imdb_movies
import os


title_basics = pd.read_csv('title_basics.tsv', sep='\t', na_values='\\N',
                            usecols=['tconst', 'primaryTitle', 'titleType', 'startYear'])


movies_ids_2020 = title_basics[(title_basics.titleType=='movie') & (title_basics.startYear==2020.0)]
movies_ids_2020 = list(movies_ids_2020['tconst'])


file_name = 'movies_df_2020.csv'


if os.path.exists(file_name):
    df = pd.read_csv(file_name, sep=';')
    next_row = len(df)
    del df
    read_imdb_movies(movies_ids_2020[next_row:], file_name)
else:
    read_imdb_movies(movies_ids_2020, file_name)
