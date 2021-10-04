path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

intro = '''
# Público, crítica y taquilla en IMDb
### Análisis exploratorio de datos | Películas 2014 a 2019
El objetivo de este estudio es buscar relaciones entre las valoraciones de usuario y de críticos del cine, y las características económicas de las películas como el presupuesto y la recaudación conseguida.
Con la intención de analizar datos representativos de todo tipo de películas se ha acudido al portal IMDb, el más completo a nivel internacional, y se han extraído los datos por dos vías: la descarga de tablas relacionales gratuitas de IMDb y mediante *web scrapping* de las películas del portal IMDb. El alcance de este estudio está limitado por la información accesible de manera gratuita en el portal IMDb, y a nivel temporal, se centra en los años comprendidos entre 2014 y 2019.
El objetivo inicial era estudiar los 10 años anteriores a 2020 (de 2010 a 2019) pero por falta de recursos solo ha sido posible recoger datos para 6 años (2014 a 2019).

### Procesos

#### 1. Tablas relacionales descargadas de IMDb
IMDb ofrece, de manera gratuita, una serie de archivos `.csv` que se corresponden con parte la información de su base de datos. De estas tablas he conseguido información como identificador de IMDb, título en español y en su versión original, duración, géneros, rating IMDb, año.

#### 2. *Web scrapping* portal IMDb
Como los archivos proporcionados por IMDb no contienen información económica de las películas he recogido esta información del propio portal IMDb mediante *web scrapping*. También era importante el dato de valoración de la crítica, el Metascore que sin ser un dato propio de IMDb sí que se puede visualizar en el portal. Además he recogido información que podría ser relevante más adelante como directores, guionistas, actores y países. Debido a la ingente cantidad de información, he tenido que utilizar la librería *parallel* para recoger información de varias páginas simultáneamente, una página por núcleo del procesador de mi portátil. La herramienta principal para esta fase fue Selenium.
> **117.482 páginas escrapeadas** (todas las películas de 2014 a 2020)

#### 3. Variables de estudio
Una vez que tenemos disponibles todos los datos seleccionamos nuestras principales variables para el estudio.
Nos encontramos con dos tipos de variables: Por un lado tenemos las variables que hacen una valoración de las películas - Rating IMDb de usuarios, Metascore- y por otra parte tenemos variabes tipo económico (Presupuesto, Recaudación, Beneficio y ROI).

#### 4. *Data mining* y *merge* de las tablas
El siguiente paso fue limpiar las tablas ya que había muchos registros *fake*, tanto en las tablas descargadas de IMDb como en el portal.
En esta fase fue necesario convertir la información escrapeada del portal ya que todo era texto. En el caso del presupuesto y la recaudación también fue necesario separar la información de la moneda y la cantidad. La moneda tuvo que ser trasladada a su código ISO para poder aisgnarle la tasa de cambio correspondiente a la moneda y el año. Finalmente normalicé los valores en dólares para todas las películas.
Y, teniendo la información de presupuesto y recaudación, generé dos nuevos datos económicos: beneficio y retorno de la inversión o ROI.

#### 5. Exploración
En esta etapa hice un análisis univariante, bivariante y multivariante de los datos de valoraciones y recaudación.
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
https://datasets.imdbws.com/

IMDb. Documentación para los datasets:
https://www.imdb.com/interfaces/

OECD. Tasas de cambio principales monedas por año:
https://data.oecd.org/conversion/exchange-rates.htm

Exchange Rates.Tasas de cambio otras monedas por año:
https://www.exchangerates.org.uk/

Google Developers. Listado de coordenadas de países:
https://developers.google.com/public-data/docs/canonical/countries_csv


'''


variables_intro = '''
## **1. Variables que puntúan las películas**
En el portal de IMDb disponemos de 3 valoraciones para cada película:
- **IMDb Rating** (asociado al número de votos para este rating)
- **Metascore**
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


## **2. Variables económicas**
En IMDb tenemos 4 variables de tipo económico:
- Presupuesto
- Recaudación del primer fin de semana en EEUU y Canadá
- Recaudación en EEUU y Canadá
- Recaudación mundial

Para este estudio necesitaremos la información de presupuesto y recaudación. Esta decisión ha propiciado prescindir de muchos registros porque solo 1.553 películas tenían estas 4 variables.

Y además crearemos otras dos nuevas, que serán Beneficio y Retorno de la Inversión, con la siguiente información:

    Beneficio = Recaudación mundial - Presupuesto

    ROI = (Recaudación mundial - Presupuesto) / Presupuesto

Finalmente, las variables económicas escogidas para cada película son:
- **Presupuesto**
- **Recaudación** (mundial)
- **Beneficio**
- **ROI**
'''


variables_intro_rating = '''
Visualizando la distribución del Rating de IMDb podemos observar que los usuarios tienden a aprobar las películas. Así, la media y la mediana se situan en `6,37` y `6,4` puntos respectivamente. El valor mínimo es de `1,40` y el máximo de `8,6`, por lo que vemos que los usuarios no dejan de ser exigentes y el promedio de la puntuación máxima no se acerca a la puntuación máxima posible: `10`.
'''

variables_intro_metascore = '''
Podemos observar que las puntuaciones de la crítica son más dispersas que el Rating de usuarios, e incluso llegan a otorgar las puntuaciones míninma y máxima de `1` y `100` puntos. Seguramente esto se deba a cómo está desarrollado el algoritmo de Metacritic que otorga estas puntuaciones de una manera automatizada. Dentro de nuestro dataset la película con el máximo Metascore es 'Boyhood' de 2014 que, sorprendentemente, consigue la puntuacion perfecta: `100`.
'''

variables_intro_presupuesto = '''
Aunque en este período de tiempo tenemos unas de las películas más caras de la historia del cine, vemos que la mayoría se situan por debajo de los 13,5 millones de dólares. 'Vengadores: Endgagme' es la película con mayor presupuesto con 378 millones de dólares.
'''


variables_intro_recaudacion = '''

'''

variables_intro_beneficio = '''
Nuevamente, la película con el máximo valor o mayor beneficio es 'Vengadores: Endgame' con más de 2.400 millones de dólares. Sin embargo, vemos que un gran porcentaje de las películas dan pérdidas con valores negativos para el beneficio. El 25% de las películas tienen una pérdidas de al menos 3 millones de dólares, y la mediana se sitúa en 4,3 millones de dólares.
'''

variables_intro_roi = '''
El ROI, al tratarse de una variable independiente del presupuesto de la película, ya nos muestra un listado de películas totalmente diferente en lo alto de la tabla. En este caso hemos tenido que limitar el listado a películas con un valor máximo de 30 ya que detectamos que había datos no válidos en algunos casos. Sorprendente la cantidad de películas de terror o thriller en las primeras posiciones.
'''