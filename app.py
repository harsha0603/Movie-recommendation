from flask import Flask, render_template,request
import pickle
import os
import pandas as pd 

app = Flask(__name__)


with open(os.path.join('models', 'movies.pkl'), 'rb') as file:
    movies_dict = pickle.load(file)

with open(os.path.join('models', 'similarity.pkl'), 'rb') as file:
    similarity = pickle.load(file)

movies = pd.DataFrame(movies_dict)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distan = similarity[index]
    movies_list = sorted(list(enumerate(distan)),reverse=True,key=lambda x:x[1])[1:6]

    remommended_movies = []
    
    for i in movies_list:
        remommended_movies.append(movies.iloc[i[0]][1])

    return remommended_movies

@app.route('/')
def home():
    titles = movies['title'].values
    return render_template('index.html',titles=titles)

@app.route('/search', methods=['POST'])
def search():
    selected_movie = request.form['movie']
    recommended_movies = recommend(selected_movie)
    return render_template('index.html', recommended_movies=recommended_movies)



if __name__ == '__main__':
    app.run(debug=True)
