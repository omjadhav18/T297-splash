import pandas as pd
import joblib  
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

MODEL_PATH = "shop_ranking/trained_model.pkl"

def train_shop_ranking_model(shop_feedback_df_for_training):

    features = ['avg_rating', 'dummy_distance_score']
    target = 'avg_rating'

    shop_avg_ratings = shop_feedback_df_for_training.groupby('shop_id')['feedback_rating'].mean().reset_index()
    shop_avg_ratings.rename(columns={'feedback_rating': 'avg_rating'}, inplace=True)

    train_df = pd.merge(shop_feedback_df_for_training, shop_avg_ratings, on='shop_id', how='left')
    train_df['dummy_distance_score'] = train_df['shop_id'].apply(lambda shop_id: abs(hash(shop_id)) % 10)

    X = train_df[features]
    y = train_df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Ridge()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"Model trained! RMSE: {rmse:.4f}")

    joblib.dump(model, MODEL_PATH)

def get_shop_ranking_score(shop_id, shop_feedback_df):
    

    model = joblib.load(MODEL_PATH)

    shop_avg_ratings = shop_feedback_df[shop_feedback_df['shop_id'] == shop_id]['feedback_rating'].mean()
    avg_rating = shop_avg_ratings if pd.notna(shop_avg_ratings) else 3.0  

    dummy_distance_score = abs(hash(shop_id)) % 10

    features_df = pd.DataFrame({'avg_rating': [avg_rating], 'dummy_distance_score': [dummy_distance_score]})
    
    return model.predict(features_df)[0]  