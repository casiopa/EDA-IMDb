path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

intro = '''
# Público, crítica y taquilla en IMDb
### Análisis exploratorio de datos | Películas 2014 a 2019
El objetivo de este estudio es buscar relaciones entre las valoraciones de usuario y de críticos del cine, y las características económicas de las películas como el presupuesto y la recaudación conseguida.
Con la intención de analizar datos representativos de todo tipo de películas se ha acudido al portal IMDb, el más completo a nivel internacional, y se han extraído los datos por dos vías: la descarga de tablas relacionales gratuitas de IMDb y mediante *web scarapping* de las películas del portal IMDb. El alcance de este estudio está limitado por la información accesible de manera gratuita en el portal IMDb, y a nivel temporal, se centra en los años comprendidos entre 2014 y 2019.
El objetivo inicial era estudiar los 10 años anteriores a 2020 (de 2010 a 2019) pero por falta de recursos solo ha sido posible recoger datos para 6 años (2014 a 2019).

### Principales procesos

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



variables_intro = '''
## Valoración de las películas
Disponemos de 3 puntuaciones para cada película:
- IMDb Rating (asociado al número de votos para este rating)
- Metascore
- Popularity


#### IMDb Rating
Esta es el promedio de las valoraciones que hacen los usuarios del portal IMDb para cada película. El rango de esta puntuación se encuentra entre 1 y 10.

Asumimos que el rating es un dato que sigue variando, sigue disponible para que el usuario vote. No disponemos del rating que había cuando la película estaba exhibiéndose en las salas, pero en esa época es cuando más votaciones recibe. Es posible que cada película, tras la emisión por televisión, reciba otra ola de votaciones, pero es cierto que al ser las películas más recientes de 2019 estos impactos ya habrán afectado a los datos recogidos ahora, en julio de 2021.

#### Metascore
Metacritic es un portal web que recopila críticas de películas, series, programas de televisión, videojuegos y libros. Metacritic ha desarrollado un algoritmo que convierte cada crítica en un porcentaje y hace una media ponderada para tener en cuenta el caché de la publicación. Esto da como resultado el metascore, una puntuación del 0 al 100 para cada producto, en nuestro caso de estudio, para cada película. 
El metascore es habitualmente utilizado por los medios como referencia para medir la recepción de la crítica.
En la página de IMDb aparece este índice para cada película y en este estudio lo tomaremos en cuenta como referencia para evaluar la valoración que hace la crítica de las películas.

#### Popularity
Dato que vamos a descartar porque es muy volátil, se mantiene en cambio constante y, al no disponer de un histórico, no guarda relación temporal con la recaudación.


## Variables económicas
En IMDb tenemos 4 variables de tipo económico:
- Presupuesto
- Recaudación del primer fin de semana en EEUU y Canadá
- Recaudación en EEUU y Canadá
- Recaudación mundial

De estas variables utilizaremos  presupuesto y recaudación. Esta decisión ha propiciado prescindir de muchos registros porque solo 1.553 películas tenían estas 4 variables.

Y además crearemos otras dos nuevas, que serán Beneficio y Retorno de la Inversión, con la siguiente información:

    \\(Beneficio = Recaudación mundial - Presupuesto\\)

    \\(ROI = (Recaudación mundial - Presupuesto) / Presupuesto\\)

Finalmente, las variables económicas escogidas para cada película son:
- Presupuesto
- Recaudación (mundial)
- Beneficio
- ROI
'''