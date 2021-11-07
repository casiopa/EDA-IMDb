# Público, crítica y taquilla en IMDb
[Enlace a dashboard interactivo `Streamlit EDA-IMDb`](https://share.streamlit.io/casiopa/eda-imdb/main/src/utils/streamlit/EDA_IMDb_main.py).

Este dashboard ha sido seleccionado por Streamlit para su galería de Visualización durante el mes de octubre de 2021.

![Streamlit EDA IMDb](https://repository-images.githubusercontent.com/390416155/3c606342-7ee0-47b4-9fb1-48008ef4039c)

### Análisis exploratorio de datos | Películas 2014 a 2019
Con la intención de analizar un dataset representativo de todo tipo de películas he acudido al portal IMDb, el más completo a nivel internacional. Y he extraído los datos por dos vías: 

##### 1. Tablas relacionales descargadas de IMDb
IMDb ofrece, de manera gratuita, una serie de archivos `.csv` que se corresponden con parte la información de su base de datos. De estas tablas he conseguido información como identificador de IMDb, título en español y en su versión original, duración, géneros, rating IMDb, año.

##### 2. *Web scrapping* portal IMDb
Como los archivos proporcionados por IMDb no contienen información económica de las películas he recogido esta información del propio portal IMDb mediante *web scrapping*. También era importante el dato de valoración de la crítica, el Metascore que sin ser un dato propio de IMDb sí que se puede visualizar en el portal. Además he recogido información que podría ser relevante más adelante como directores, guionistas, actores y países. Debido a la ingente cantidad de información, he tenido que utilizar *parallel* para recoger información de varias páginas simultáneamente, una página por núcleo del procesador de mi portátil. La herramienta principal para esta fase fue Selenium.
> **117.482 páginas escrapeadas** (todas las películas de 2014 a 2020)

#### 3. *Variables* de estudio
Una vez que tenemos disponibles todos los datos seleccionamos nuestras principales variables para el estudio.
Nos encontramos con dos tipos de variables: Por un lado tenemos las variables que hacen una valoración de las películas - Rating IMDb de usuarios, Metascore- y por otra parte tenemos variabes tipo económico (Presupuesto, Recaudación, Beneficio y ROI).

##### 4. *Data mining* y *merge* de las tablas
El siguiente paso fue limpiar las tablas ya que había muchos registros *fake*, tanto en las tablas descargadas de IMDb como en el portal.
En esta fase fue necesario convertir la información escrapeada del portal ya que todo era texto. En el caso del presupuesto y la recaudación también fue necesario separar la información de la moneda y la cantidad. La moneda tuvo que ser trasladada a su código ISO para poder aisgnarle la tasa de cambio correspondiente a la moneda y el año. Finalmente normalicé los valores en dólares para todas las películas.
Y, teniendo la información de presupuesto y recaudación, generé dos nuevos datos económicos: beneficio y retorno de la inversión o ROI.

##### 5. Exploración
En esta etapa hice un análisis univariante, bivariante y multivariante de los datos de valoraciones y recaudación.


---
## Herramientas utilizadas

| Web scrapping 		    | Data mining		    | Visualización  	|
|---			      		|---		    		|---		      	|
| - Visual Studio Code	    | - Jupyter Lab		    | - Streamlit		|
| - Python				    | - Python			    | - Python			|
| - Pandas				    | - Regex			    | - Regex			|
| - Selenium			    | - Pandas			    | - Pandas			|
| - Joblib / Parallel	    | - Numpy			    | - Numpy			|
| - Logging				    |   				    | - Matplotlib		|
| - Pickle				    |   				    | - Plotly			|
|   					    |   				    | - Google Slides	|

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
