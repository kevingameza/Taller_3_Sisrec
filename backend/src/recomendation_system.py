from sqlalchemy.orm import Session
from joblib import load
from surprise import Dataset, Reader, accuracy, Prediction
from surprise.model_selection import train_test_split
import pandas as pd
import networkx as nx

modelo = load('algo_cosine_model.joblib')

dataRatingsFiltered = pd.read_csv('/backend/csv-data/dataRatingsFiltered.csv')
reader = Reader(rating_scale=(dataRatingsFiltered['rating'].min(), dataRatingsFiltered['rating'].max()))
data = Dataset.load_from_df(dataRatingsFiltered[['userId', 'movieId', 'rating']], reader)

# df_review = pd.read_csv('/backend/csv-data/df_review.csv')
# surprise_dataset = Dataset.load_from_df(df_review[['user_id', 'business_id', 'stars']], reader)
# trainset = surprise_dataset.build_full_trainset()


df_final = pd.read_csv('/backend/csv-data/resultados_peliculas_genres.csv')
# Crear un grafo para representar las relaciones ontológicas
G = nx.Graph()

# Función para agregar relaciones al grafo
def agregar_relaciones_ontologicas(movie, graph):
    actors = set(movie['stars'].split(', '))
    directors = set(movie['directors'].split(', '))
    genres= set(movie['genres'].split('|'))

    for actor in actors:
        graph.add_edge(movie['film_title'], actor, relation='actor')
    for director in directors:
        graph.add_edge(movie['film_title'], director, relation='director')
    for genre in genres:
        graph.add_edge(movie['genres'], genre, relation='genres')

# Agregar relaciones ontológicas al grafo
for index, row in df_final.iterrows():
    agregar_relaciones_ontologicas(row, G)

# Función para calcular la similitud ontológica entre películas basada en el grafo
def calcular_similitud_ontologica_graph(movie1, movie2, graph):
    shortest_paths = []
    for actor1 in set(movie1['stars'].split(', ')):
        for actor2 in set(movie2['stars'].split(', ')):
            try:
                shortest_path = nx.shortest_path_length(graph, source=actor1, target=actor2)
                shortest_paths.append(shortest_path)
            except nx.NetworkXNoPath:
                pass

    for director1 in set(movie1['directors'].split(', ')):
        for director2 in set(movie2['directors'].split(', ')):
            try:
                shortest_path = nx.shortest_path_length(graph, source=director1, target=director2)
                shortest_paths.append(shortest_path)
            except nx.NetworkXNoPath:
                pass

    for genre1 in set(movie1['genres'].split('|')):
        for genre2 in set(movie2['genres'].split('|')):
            try:
                shortest_path = nx.shortest_path_length(graph, source=genre1, target=genre2)
                shortest_paths.append(shortest_path)
            except nx.NetworkXNoPath:
                pass

    return min(shortest_paths, default=float('inf'))


# Función de recomendación basada en filtraje ontológico con el grafo y calificación
def recomendar_peliculas_calificadas(movie_title, df=df_final, graph=G, top_n=5):
    movie = df[df['film_title'] == movie_title].iloc[0]
    similarities = []
    for index, row in df.iterrows():
        if row['film_title'] != movie_title:
            similarity = calcular_similitud_ontologica_graph(movie, row, graph)
            # Asignar una puntuación basada en la inversa de la similitud
            score = (1 / (similarity + 1))*5  # Añadimos 1 para evitar divisiones por cero
            similarities.append((row['film_title'], similarity, score))

    similarities = sorted(similarities, key=lambda x: x[2], reverse=True)  # Ordenar por puntuación descendente
    recommendations = [(title, score) for title, _, score in similarities[:top_n]]
    return recommendations

# Probar la función de recomendación calificada
recommendations = recomendar_peliculas_calificadas('A Quiet Place', df_final, G, 3)
print(recommendations)


def get_top_n_recommendations_model(user_id, top_n: int = 5):

    user_movies = dataRatingsFiltered[dataRatingsFiltered['userId'] == user_id]['movieId'].unique()
        # Obtener los títulos de las películas vistas por el usuario
    user_movie_titles = df_final[df_final['movieId'].isin(user_movies)]['movieId']
    # Obtener las películas que el usuario no ha visto
    unseen_movies = [movie_id for movie_id in user_movie_titles ]
    # Predecir las calificaciones para todas las películas no vistas
    predictions = [modelo.predict(uid=user_id, iid=movie_id) for movie_id in unseen_movies]
    # Ordenar las predicciones por la calificación estimada en orden descendente
    predictions.sort(key=lambda x: x.est, reverse=True)
    # Obtener las 10 mejores predicciones
    top_n_predictions = predictions[:top_n]
    return top_n_predictions


