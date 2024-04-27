from sqlalchemy.orm import Session
from joblib import load
from surprise import Dataset, Reader, accuracy, Prediction
from surprise.model_selection import train_test_split
import pandas as pd

modelo_knn = load('modelo_knnbasic.joblib')
modelo_svd = load('modelo_svd.joblib')

reader = Reader(rating_scale=(1, 5))
df_review = pd.read_csv('/backend/csv-data/df_review.csv')
surprise_dataset = Dataset.load_from_df(df_review[['user_id', 'business_id', 'stars']], reader)
trainset = surprise_dataset.build_full_trainset()


class RecommendationResponse:
    def __init__(self, user_id, business_id, stars):
        self.user_id = user_id
        self.business_id = business_id
        self.stars = stars

def get_recommendation(user_id:str, business_id:str):
    print('--------------------------------')
    predicciones_svd = modelo_svd.predict(user_id, business_id)
    predicciones_knn = modelo_knn.predict(user_id, business_id)
    promedio_est = (predicciones_svd.est + predicciones_knn.est) / 2

    return promedio_est

def get_top_n_recommendations(user_id: str, n: int = 10):
    print('--------------------------------')

    unique_businesses = df_review['business_id'].unique()
    predictions = []

    for business_id in unique_businesses:
        pred_svd = modelo_svd.predict(user_id, business_id)
        pred_knn = modelo_knn.predict(user_id, business_id)
        avg_rating = (pred_svd.est + pred_knn.est) / 2
        predictions.append((business_id, avg_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_n_predictions = predictions[:n]

    return [RecommendationResponse(user_id, business_id, stars) for business_id, stars in top_n_predictions]
