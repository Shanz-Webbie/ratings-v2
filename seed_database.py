"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

# create and drop database
os.system("dropdb ratings")
os.system("createdb ratings")
# connect to database
connect_to_db(app)
app.app_context().push()
db.create_all()
# load and save data
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # get the title, overview, and poster_path from the movie dict
    title, overview, poster_path =(
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    # get the release_date and convert it to a
    # datetime object with datetime.strptime
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    # create a movie here and append it to movies_in_db
    film = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(film)
for n in range(10):
    email = f'user{n + 1}@test.com'  # Voila! A unique email!
    password = 'test'
    # create 10 users
    user = crud.create_user(email, password)
    db.session.add(user)
for i in range(10):
    #create 10 ratings for the user(s)
    random_movie = choice(movies_in_db)
    score = randint(1, 5)
    rating = crud.create_rating(user, random_movie, score)
    db.session.add(rating)

# adding movies from the list
db.session.add_all(movies_in_db)
# commiting all changes to the session
db.session.commit()