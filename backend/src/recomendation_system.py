from sqlalchemy.orm import Session
from joblib import load
from surprise import Dataset, Reader, accuracy, Prediction
from surprise.model_selection import train_test_split
import pandas as pd
import networkx as nx

modelo = load('algo_cosine_model.joblib')

dataRatingsFiltered = pd.read_csv('../csv-data/dataRatingsFiltered.csv')
reader = Reader(rating_scale=(dataRatingsFiltered['rating'].min(), dataRatingsFiltered['rating'].max()))
data = Dataset.load_from_df(dataRatingsFiltered[['userId', 'movieId', 'rating']], reader)

# df_review = pd.read_csv('/backend/csv-data/df_review.csv')
# surprise_dataset = Dataset.load_from_df(df_review[['user_id', 'business_id', 'stars']], reader)
# trainset = surprise_dataset.build_full_trainset()


df_final = pd.read_csv('../csv-data/resultados_peliculas_genres.csv')
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
def recomendar_peliculas_calificadas(movie_title, df, graph, top_n=5):
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


# def get_recommendation(user_id:str, business_id:str):
#     print('--------------------------------')
#     predicciones_svd = modelo_svd.predict(user_id, business_id)
#     predicciones_knn = modelo_knn.predict(user_id, business_id)
#     promedio_est = (predicciones_svd.est + predicciones_knn.est) / 2

#     return promedio_est

# def get_top_n_recommendations(user_id: str, n: int = 10):
#     print('--------------------------------')

#     unique_businesses = df_review['business_id'].unique()
#     predictions = []

#     for business_id in unique_businesses:
#         pred_svd = modelo_svd.predict(user_id, business_id)
#         pred_knn = modelo_knn.predict(user_id, business_id)
#         avg_rating = (pred_svd.est + pred_knn.est) / 2
#         predictions.append((business_id, avg_rating))

#     predictions.sort(key=lambda x: x[1], reverse=True)
#     top_n_predictions = predictions[:n]

#     return [RecommendationResponse(user_id, business_id, stars) for business_id, stars in top_n_predictions]
