path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

intro = '''
# Público, crítica y taquilla en IMDb
### Análisis exploratorio de datos | Películas 2014 a 2019
Con la intención de analizar un dataset representativo de todo tipo de películas he acudido al portal IMDb, el más completo a nivel internacional. Y he extraído los datos por dos vías: 

#### 1. Tablas relacionales descargadas de IMBd
IMDb ofrece, de manera gratuita, una serie de archivos `.csv` que se corresponden con parte la información de su base de datos. De estas tablas he conseguido información como identificador de IMDb, título en español y en su versión original, duración, géneros, rating IMDb, año.

#### 2. *Web scrapping* portal IMBd
Como los archivos proporcionados por IMDb no contienen información económica de las películas he recogido esta información del propio portal IMDb mediante *web scrapping*. También era importante el dato de valoración de la crítica, el Metascore que sin ser un dato propio de IMBd sí que se puede visualizar en el portal. Además he recogido información que podría ser relevante más adelante como directores, guionistas, actores y países. Debido a la ingente cantidad de información, he tenido que utilizar parallel para recoger información simultáneamente de varias páginas simultáneamente, una página por núcleo del procesador de mi portátil. La herramienta principal en esta estapa fue Selenium.
> **117.482 páginas escrapeadas** (todas las películas de 2014 a 2020)

#### 3. *Variables* de estudio
Una vez que tenemos diponible todos los datos seleccionamos nuestras principales variables para el estudio.
Nos encontramos con dos tipos de variables: Por un lado tenemos las variables que hacen una valoración de las películas - Rating IMDb de usuarios, Metascore- y por otra parte tenemos variabes tipo económico (Presupuesto, Recaudación, Beneficio y ROI).

#### 4. *Data mining* y *merge* de las tablas
El siguiente paso fue limpiar las tablas ya que había muchos registros *fake*, tanto en las tablas descargadas de IMDb como en el portal.
En esta fase fue necesario convertir la información escrapeada del portal ya que todo era texto. En el caso del presupuesto y la recaudación también fue necesario separar la información de la moneda y la cantidad. La moneda tuvo que ser trasladada al código ISO correspondiente para poder aisgnarle la tasa de cambio correspondiente a la moneda y el año. Finalmente normalicé los valores en dólares para todas las películas.
Finalmente, teniendo la información de presupuesto y recaudación, he generado dos nuevos datos que son los beneficios y el retorno de la inversión o ROI.

#### 5. Exploración
En esta etapa hice un análisis univariante, bivariante y multivariante de los datos de valoraciones y recaudación.

#### 6. Conclusiones
En el análisis podemos concluir que las valoraciones de los usuarios tienen una mayor tendencia a aprobar las películas, sin embargo las puntuaciones de la crítica son más dispersas e incluso llegan a otorgar la puntuación máxima de 100.
'''



intro_herramientas_fuentes = '''
---
## Herramientas utilizadas

| Web scrapping 		| Data mining		| Visualización  	|
|---					|---				|---				|
| - Visual Studio Code	| - Jupyter Lab		| - Streamlit		|
| - Python				| - Python			| - Python			|
| - Pandas				| - Regex			| - Regex			|
| - Selenium			| - Pandas			| - Pandas			|
| - Joblib / Parallel	| - Numpy			| - Numpy			|
| - Logging				|   				| - Matplotlib		|
| - Pickle				|   				| - Plotly			|
|   					|   				| - Google Slides	|

<p><br></p>

---
## Fuentes

IMDd Datasets
https://www.imdb.com/interfaces/

IMDb. Documentación para los datasets:
https://www.imdb.com/interfaces/

OECD. Tasas de cambio principales monedas por año:
https://data.oecd.org/conversion/exchange-rates.htm

Exchange Rates.Tasas de cambio otras monedas por año:
https://www.exchangerates.org.uk/

Google Developers. Listado de coordenadas de países:
https://developers.google.com/public-data/docs/canonical/countries_csv

Posible map for countries after clean and merge dataframes of years:
https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10


'''