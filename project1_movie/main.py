import ast
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

# Input data files are available in format read-only
movies = pd.read_csv("C:\\Users\\Admin01\\Downloads\\MISC\Machine Learnin Project\\project1\\tmdb_5000_movies.csv")
credits = pd.read_csv("C:\\Users\\Admin01\\Downloads\\MISC\Machine Learnin Project\\project1\\tmdb_5000_credits.csv")

# info about the dataframe

# print(movies.head(1))
# print(credits.head(1))
# print(movies.merge(credits, on='title').shape)
# print(credits.shape)

# merging both movies datagrame
movies = movies.merge(credits, on='title')

# print(movies['original_language'].value_counts())
# print(movies.info)

# checking null
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
print(movies.isnull().sum())

# drop null
movies.dropna(inplace=True)
print(movies.isnull().sum())
print(movies.duplicated().sum())


# converting string (genres,keyword,etc...) to list
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L


movies['genres'] = movies['genres'].apply(convert)
print(movies.head())
movies['keywords'] = movies['keywords'].apply(convert)
print(movies.head())

ast.literal_eval(
    '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, '
    '"name": "Science Fiction"}]')

# def convert3(text):
#     L = []
#     counter = 0
#     for i in ast.literal_eval(text):
#         if counter < 3:
#             L.append(i['name'])
#         counter += 1
#     return L


movies['cast'] = movies['cast'].apply(convert)
movies.head()
movies['cast'] = movies['cast'].apply(lambda x: x[0:3])


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L


# collecting crew members
movies['crew'] = movies['crew'].apply(fetch_director)
movies.sample(5)


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ", ""))
    return L1


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
new = movies[['movie_id', 'title', 'tags']]
new['tags'] = new['tags'].apply(lambda x: " ".join(x))
# new_df['tags'].apply(lambda x:" ".join(x))
new['tags'] = new['tags'].apply(lambda x: x.lower())

# use this for suffixes the tags we created and helps in filtering
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


print(new.head(1))

# ml
# training the model
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()
print(vector.shape)

new['tags'].apply(stem)

similarity = cosine_similarity(vector)
print(similarity)


# recomending the movie

def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:8]:
        print(new.iloc[i[0]].title)


print(recommend('Avatar'))

# pickle.dump(new,open('movie_list.pkl','wb'))
pickle.dump(new.to_dict(), open("movie_list.pkl", 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
