from collections import Counter
import wordcloud as wordcloud
import pandas as pd
import seaborn as sns
import missingno
import matplotlib.pyplot as plt
import scipy as sp
import plotly.express as px
import squarify as squarify
import statsmodels.api as sm

# read csv file
from wordcloud import WordCloud

df_credits = pd.read_csv("C:\\Users\\Admin01\\Downloads\\MISC\\Machine Learnin Project\\project1\\tmdb_5000_credits.csv")
df_movies = pd.read_csv("C:\\Users\\Admin01\\Downloads\\MISC\\Machine Learnin Project\\project1\\tmdb_5000_movies.csv")

# df_movies.genres = df_movies.genres.str.split(",",n=2,expand=True)[1]
# df_movies.genres.dropna(inplace=True)
#
# # Extract year from release date
# df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])
# df_movies['year'] = df_movies['release_date'].dt.year
# df_movies.year = df_movies.year.fillna(0).astype(int)
# df_movies.groupby('genres').revenue.sum().nlargest(3)
# # For category- Action, plot the last 10 years moving average trend
# df_action = df_movies.query('genres == "Action"').groupby('year').revenue.sum()
# df_action = df_action.rolling(window=10).mean()

# df_movie_small = df_movies[['year','production_companies','revenue']]
# df_new = df_movie_small.loc[df_movie_small.groupby(['year']).revenue.idxmax()]
# df_new = df_new.groupby('production_companies').year.count()
# df_new = df_new[df_new > 1]
# df_new.plot(kind='bar', stacked=True, colormap='autumn')

# viewing the coloums
print(df_movies.columns)
print(df_credits.columns)

# DataFrame information , this says the types of data
print(df_movies.info())
print(df_credits.info())
# stats value of dataframe
print(df_credits.describe())
print(df_movies.describe())

# corr the dataframe
print(df_movies.corr(method='pearson'))
print(df_credits.corr(method='pearson'))
'''They can tell us about the direction of the relationship, the form (shape) of the relationship, and the degree (
strength) of the relationship between two variables.The Direction of a Relationship The correlation measure tells us 
about the direction of the relationship between the two variables. Any na values are automatically excluded 
-1 indicates a perfectly negative linear correlation between two variables
0 indicates no linear correlation between two variables
1 indicates a perfectly positive linear correlation between two variables
'''

# finding null in the dataframe
print(df_credits.isna().sum())
print(df_movies.isna().sum())
# df_credits has no null values

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
# fig3, ax3 = plt.subplots()
# missing value chart
missingno.bar(df_movies, fontsize=10, figsize=(10, 5), color="dodgerblue", sort="ascending", ax=ax1)
ax1.set_title('COLUMN WISE VALUES', fontsize=20)

# drop missing coloums
df_movies.dropna(inplace=True)

# corr heatmap chart
# df_credits only movie_id will co-relate as there are fewer columns ,  as we saw above
ax2.set_title('DataFrame Corr-Heatmap', fontsize=15)
sns.heatmap(df_movies.corr(), ax=ax2, linewidths=.5, cmap="YlGnBu", cbar=True, square=True, annot=True, center=0)

# relation between the budget and revenue
# using ploty
# fig = px.scatter(df_moviess, x="budget", y="revenue", trendline="ols", title="Relationship between Budget and Revenue")
# fig.update_layout(xaxis_title="Budget",
#                  yaxis_title="Revenue")
# fig.show()


g = sns.lmplot(x='budget', y='revenue', data=df_movies,
               height=3, aspect=1)


def annotate(data, **kws):
    r, p = sp.stats.pearsonr(data['revenue'], data['budget'])
    ax = plt.gca()
    ax.text(.5, .8, 'r={:.2f}, p={:.2g}'.format(r, p),
            transform=ax.transAxes)


g.map_dataframe(annotate)

'''sizes = Counter(prime['Age of viewers']).values()
labels = Counter(prime['Age of viewers']).keys()

explode = (0.1, 0.1, 0.1, 0.1, 0.1)

# Creating color parameters 
colors = ("orange", "lightcoral",
          "lightskyblue", "yellowgreen", "beige")
# Plot
plt.figure(figsize=(8, 8))
plt.title("Viewership Age - All vs Rest", fontweight='bold')
plt.pie(sizes, explode=explode, labels=labels, colors=colors, shadow=True, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.show()'''

# #genres tree map
# print(df_moviess['genres'][1])

# most uploaded language
language_info = df_movies["original_language"].value_counts()[:50]
wordcloud = WordCloud(background_color='black')
wordcloud.generate_from_frequencies(dict(language_info))
plt.figure(figsize=(15, 10))
plt.title("origin langiage", fontsize=25, pad=20)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off");

plt.show()
