'''
author : Jaydatt Patel
Coursera : Data Collection and Processing with Python by University of Michigan
Week 3 Final Project - OMDB and TasteDive Mashup
'''

#Your first task will be to fetch data from TasteDive. The documentation for the API is at https://tastedive.com/read/api.
# Define a function, called get_movies_from_tastedive. It should take one input parameter, a string that is the name of a movie or music artist. The function should return the 5 TasteDive results that are associated with that string; be sure to only get movies, not other kinds of media. It will be a python dictionary with just one key, ‘Similar’.
# Try invoking your function with the input “Black Panther”.
# HINT: Be sure to include only q, type, and limit as parameters in order to extract data from the cache. If any other parameters are included, then the function will not be able to recognize the data that you’re attempting to pull from the cache. Remember, you will not need an api key in order to complete the project, because all data will be found in the cache.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching

def get_movies_from_tastedive(movie, type='movies',limit='5'):
    params = {}
    params['q'] = movie
    params['type'] = type
    params['limit'] = limit
    baseurl = 'https://tastedive.com/api/similar'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json()

get_movies_from_tastedive("Bridesmaids")
get_movies_from_tastedive("Black Panther")


# Please copy the completed function from above into this active code window. Next, you will need to write a function that extracts just the list of movie titles from a dictionary returned by get_movies_from_tastedive. Call it extract_movie_titles.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching

def get_movies_from_tastedive(movie, type='movies',limit='5'):
    params = {}
    params['q'] = movie
    params['type'] = type
    params['limit'] = limit
    baseurl = 'https://tastedive.com/api/similar'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json()

def extract_movie_titles(data): 
    movies = [d['Name'] for d in data['Similar']['Results']]
    return movies

extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))
extract_movie_titles(get_movies_from_tastedive("Black Panther"))

# Please copy the completed functions from the two code windows above into this active code window. Next, you’ll write a function, called get_related_titles. It takes a list of movie titles as input. It gets five related movies for each from TasteDive, extracts the titles for all of them, and combines them all into a single list. Don’t include the same movie twice.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching
def get_movies_from_tastedive(movie, type='movies',limit='5'):
    params = {}
    params['q'] = movie
    params['type'] = type
    params['limit'] = limit
    baseurl = 'https://tastedive.com/api/similar'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json()

def extract_movie_titles(data): 
    movies = [d['Name'] for d in data['Similar']['Results']]
    return movies

def get_related_titles(movies):
    all = []
    for movie in movies : 
        five = extract_movie_titles(get_movies_from_tastedive(movie))
        for m in five:
            if m not in all:
                all += [m]
    return all

get_related_titles(["Black Panther", "Captain Marvel"])
get_related_titles([])


# Your next task will be to fetch data from OMDB. The documentation for the API is at https://www.omdbapi.com/

# Define a function called get_movie_data. It takes in one parameter which is a string that should represent the title of a movie you want to search. The function should return a dictionary with information about that movie.

# Again, use requests_with_caching.get(). For the queries on movies that are already in the cache, you won’t need an api key. You will need to provide the following keys: t and r. As with the TasteDive cache, be sure to only include those two parameters in order to extract existing data from the cache.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching

def get_movie_data(movie):
    params = {}
    params['t'] = movie
    params['r'] = 'json'
    baseurl = 'http://www.omdbapi.com/'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json() 

get_movie_data("Venom")
get_movie_data("Baby Mama")


# Please copy the completed function from above into this active code window. Now write a function called get_movie_rating. It takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer. For example, if given the OMDB dictionary for “Black Panther”, it would return 97. If there is no Rotten Tomatoes rating, return 0.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching

def get_movie_data(movie):
    params = {}
    params['t'] = movie
    params['r'] = 'json'
    baseurl = 'http://www.omdbapi.com/'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json() 

def get_movie_rating(data):
    rating = 0
    for d in data['Ratings']:
        if d['Source'] == 'Rotten Tomatoes':
            rating = int(d['Value'][:-1])
    return rating

get_movie_rating(get_movie_data("Deadpool 2"))

# Now, you’ll put it all together. Don’t forget to copy all of the functions that you have previously defined into this code window. Define a function get_sorted_recommendations. It takes a list of movie titles as an input. It returns a sorted list of related movie titles as output, up to five related movies for each input movie title. The movies should be sorted in descending order by their Rotten Tomatoes rating, as returned by the get_movie_rating function. Break ties in reverse alphabetic order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages

import requests_with_caching

def get_movies_from_tastedive(movie, type='movies',limit='5'):
    params = {}
    params['q'] = movie
    params['type'] = type
    params['limit'] = limit
    baseurl = 'https://tastedive.com/api/similar'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json()

def extract_movie_titles(data): 
    movies = [d['Name'] for d in data['Similar']['Results']]
    return movies

def get_related_titles(movies):
    all = []
    for movie in movies : 
        five = extract_movie_titles(get_movies_from_tastedive(movie))
        for m in five:
            if m not in all:
                all += [m]
    return all

def get_movie_data(movie):
    params = {}
    params['t'] = movie
    params['r'] = 'json'
    baseurl = 'http://www.omdbapi.com/'
    page = requests_with_caching.get(baseurl,params=params)
    return page.json() 

def get_movie_rating(data):
    rating = 0
    for d in data['Ratings']:
        if d['Source'] == 'Rotten Tomatoes':
            rating = int(d['Value'][:-1])
    return rating

def get_sorted_recommendations(movies):
    related = get_related_titles(movies)
    dic = {}
    for movie in related:
        dic[movie] = get_movie_rating(get_movie_data(movie))
    return (sorted(dic,reverse = True,key = lambda movie : (dic[movie],movie)))

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])