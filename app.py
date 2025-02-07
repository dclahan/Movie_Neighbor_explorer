from flask import Flask, render_template, request
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}
jobs = ['Director', 'Writer', 'Original Music Composer', 'Director of Photography']
cache = {}

# Existing backend functions (slightly modified for Flask)
def searchTMDB(searchTerm):
    searchURL = f"https://api.themoviedb.org/3/search/movie?query={searchTerm}"
    if searchURL in cache:
        return cache[searchURL]
    response = requests.get(searchURL, headers=headers)
    cache[searchURL] = response
    return response

def getCredits(id):
    url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"
    if url in cache:
        return cache[url]
    response = requests.get(url, headers=headers)
    cache[url] = response
    return response

def getLinks(id):
    response = getCredits(id)
    resptext = json.loads(response.text)
    actors = {(x['id'],x['name']) for x in resptext['cast']}
    crew = {(x['id'],x['name']) for x in resptext['crew'] if x['job'] in jobs}
    return actors.union(crew)

def getMoviesByActor(pid):
    url = f'https://api.themoviedb.org/3/person/{pid}/movie_credits?language=en-US'
    if url in cache:
        response = cache[url]
    else:
        response = requests.get(url, headers=headers)
        cache[url] = response
    resptext = json.loads(response.text)
    movies = resptext['cast'] + [x for x in resptext['crew'] if x['job'] in jobs]
    return movies

def getNeighbors(id):
    links = getLinks(id)
    movs = list()
    ids = set()
    for pid, actor in links:
        for mov in getMoviesByActor(pid):
            if mov['id'] not in ids:
                mov['link'] = actor
                movs.append(mov)
                ids.add(mov['id'])
    movs.sort(key=lambda x: x['popularity'], reverse=True)
    return movs

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return render_template('index.html')
    
    response = searchTMDB(query)
    if response.status_code != 200:
        return render_template('error.html', message="API request failed")
    
    results = json.loads(response.text).get('results', [])
    return render_template('search_results.html', results=results, query=query)


@app.route('/movie/<int:movie_id>')
def movie_neighbors(movie_id):
    neighbors = getNeighbors(movie_id)[:100]
    unique_links = set()
    
    for mov in neighbors:
        mov['year'] = mov['release_date'][:4] if mov.get('release_date') else 'N/A'
        mov['poster_url'] = f"https://image.tmdb.org/t/p/original/{mov['poster_path']}" if mov.get('poster_path') else None
        unique_links.add(mov['link'])
    
    return render_template('neighbors.html', 
                         movies=neighbors,
                         unique_links=sorted(unique_links))


if __name__ == '__main__':
    app.run(debug=True)