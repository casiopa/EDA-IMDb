import pandas as pd
from selenium import webdriver
import logging
import os
from joblib import Parallel, delayed
import time


def read_imdb_movie(imdb_id):

    driver = r'C:\Users\casiopa\chromedriver.exe'
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=driver, options=options)


    url_title = 'https://www.imdb.com/title/' + str(imdb_id)
    driver.get(url_title)


    try:
        principal_credits = driver.find_element_by_class_name('PrincipalCredits__PrincipalCreditsPanelWideScreen-hdn81t-0').find_element_by_tag_name('ul')

        directors = []
        elements_directors = principal_credits.find_elements_by_xpath("//li[@data-testid='title-pc-principal-credit']")[0] \
                            .find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')

        for director in elements_directors:
            directors.append(director.find_element_by_tag_name('a').text)
    except:
        directors = 'NaN'

        
    try:    
        writers = []
        elements_writers = principal_credits.find_elements_by_xpath("//li[@data-testid='title-pc-principal-credit']")[1]  \
                                    .find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        for writer in elements_writers:
            writers.append(writer.find_element_by_tag_name('a').text)
    except:
        writers = 'NaN'

        
    try:    
        stars = []
        elements_stars = principal_credits.find_elements_by_xpath("//li[@data-testid='title-pc-principal-credit']")[2]  \
                                    .find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        for star in elements_stars:
            stars.append(star.find_element_by_tag_name('a').text)
    except:
        stars = 'NaN'

        
    try:
        title = driver.find_element_by_tag_name('h1').text
    except:
        title = 'NaN'
        
        
    try:
        original_title = driver.find_element_by_class_name('OriginalTitle__OriginalTitleText-jz9bzr-0').text.replace('Original title: ', '')
    except:
        original_title = 'NaN'
        
        
    try:    
        year = driver.find_element_by_class_name('TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2') \
            .find_element_by_tag_name('ul').find_element_by_tag_name('li').find_element_by_tag_name('a').text
    except:
        year = 'NaN'
        
        
    try:    
        certificate = driver.find_element_by_class_name('TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2') \
                    .find_element_by_tag_name('ul').find_elements_by_tag_name('li')[1].find_element_by_tag_name('a').text
    except:
        certificate = 'NaN'
        
        
    try:    
        duration = driver.find_element_by_class_name('TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2') \
                .find_element_by_tag_name('ul').find_elements_by_tag_name('li')[2].text
    except:
        duration = 'NaN'
        
        
    try:
        imdb_rating = driver.find_element_by_class_name('AggregateRatingButton__RatingScore-sc-1ll29m0-1').text
    except:
        imdb_rating = 'NaN'
        
    try:
        imdb_rating_counts = driver.find_element_by_class_name('AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3').text
    except:
        imdb_rating_counts = 'NaN'
        
    try:    
        metascore = driver.find_element_by_class_name('score-meta').text
    except:
        metascore = 'NaN'

    try:
        popularity = driver.find_element_by_class_name('TrendingButton__TrendingScore-bb3vt8-1').text
    except:
        popularity = 'NaN'


    try:
        awards = driver.find_element_by_class_name('Awards__Content-sc-1qdt65t-2').text
    except:
        awards = 'NaN'

    try:
        budget = driver.find_element_by_xpath('//li[@data-testid="title-boxoffice-budget"]').find_elements_by_tag_name('span')[1].text.replace(' (estimated)', '')
    except:
        budget = 'NaN'


    try:
        gross_us_canada = driver.find_element_by_xpath('//li[@data-testid="title-boxoffice-grossdomestic"]').find_elements_by_tag_name('span')[1].text
    except:
        gross_us_canada = 'NaN'
        
    try:    
        opening_us_canada = driver.find_element_by_xpath('//li[@data-testid="title-boxoffice-openingweekenddomestic"]').find_elements_by_tag_name('span')[1].text
    except:
        opening_us_canada = 'NaN'
        
    try:    
        gross_world = driver.find_element_by_xpath('//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]').find_elements_by_tag_name('span')[1].text
    except:
        gross_world = 'NaN'



    try:
        countries = []
        for country in driver.find_elements_by_xpath("//li[@data-testid='title-details-origin']")[0].find_elements_by_tag_name('a'):
            countries.append(country.text)
    except:
        countries = 'NaN'

    try:
        companies = []
        for company in driver.find_elements_by_xpath("//li[@data-testid='title-details-companies']")[0].find_element_by_tag_name('div').find_elements_by_tag_name('a'):
            companies.append(company.text)
    except:
        companies = 'NaN'



        
        
    # Genre needs 2 tries   
    try:
        genres = []
        for elem in driver.find_elements_by_class_name('GenresAndPlot__GenresChipList-cum89p-4'):
            for genre in elem.find_elements_by_tag_name('a'):
                genres.append(genre.text)
    except:
        genres = 'NaN'
        
    if genres == []:    
        try:
            genres = []
            for elem in driver.find_elements_by_class_name('GenresAndPlot__OffsetChipList-cum89p-5'):
                for genre in elem.find_elements_by_tag_name('a'):
                    genres.append(genre.text)
        except:
            pass



    driver.close()
    
    return {'imdb_id': imdb_id,
            'title': title,
            'original_title': original_title,
            'year': year,
            'certificate': certificate,
            'duration': duration,
            'directors': directors,
            'writers': writers,
            'stars': stars,
            'genres': genres,
            'countries': countries,
            'companies': companies,
            'imdb_rating': imdb_rating,
            'metascore': metascore,
            'popularity': popularity,
            'awards': awards,
            'budget': budget,
            'gross_us_canada': gross_us_canada,
            'opening_us_canada': opening_us_canada,
            'gross_world': gross_world
           }


def bucle(movies_df, file_name, idx, movie_id):
    movie = read_imdb_movie(movie_id)
    print(idx, movie['imdb_id'])
    movies_df = movies_df.append(movie, ignore_index=True)
    movies_df.to_csv(file_name, sep=';', mode ='a', index=False, header=not os.path.exists(file_name))

    msg = str(idx+1) + ' películas escritas en CVS ' + file_name
    logging.info(msg)
        


def read_imdb_movies(movies_id, file_name, cores):



    movies_df = pd.DataFrame(columns = ['imdb_id', 'title', 'original_title', 'year', 'certificate', 'duration','directors',
                                    'writers', 'stars', 'genres', 'countries', 'companies', 'imdb_rating', 'metascore',
                                    'popularity', 'awards', 'budget', 'gross_us_canada','opening_us_canada', 'gross_world'])


    # Creación del logger que muestra la información únicamente por fichero.
    logging.basicConfig(
        format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
        level  = logging.INFO,      # Nivel de los eventos que se registran en el logger
        filename = "logs_info.log", # Fichero en el que se escriben los logs
        filemode = "a"              # a ("append"), en cada escritura, si el archivo de logs ya existe,
                                    # se abre y añaden nuevas lineas.
    )


    Parallel(n_jobs=cores)(delayed(bucle)(movies_df, file_name, idx, movie_id) for idx, movie_id in enumerate(movies_id))

    
    logging.shutdown()




