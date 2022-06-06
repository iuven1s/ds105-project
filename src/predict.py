import pandas as pd
import numpy as np
import pickle
from api_functions import *


token = get_access_token(CLIENT_ID, CLIENT_SECRET)
GENRES = ['classical', 'country', 'edm', 'hip-hop', 'jazz', 'pop', 'rap', 'rnb', 'rock']
GENRE_LIST = {
    0: 'Classical',
    1: 'Country',
    2: 'EDM',
    3: 'Hip-hop',
    4: 'Jazz',
    5: 'Pop',
    6: 'Rap',
    7: 'RnB',
    8: 'Rock'
}


def get_audio_features(track_id):
    track_features = pd.DataFrame(general_endpoint(BASE_URL + f'audio-features/{track_id}', headers=token), index=[track_id,])
    track_features.drop(['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1, inplace=True)
    track_features.drop(['energy', 'acousticness'], axis=1, inplace=True)
    return track_features


def normalise(track_id):
    track_features = get_audio_features(track_id)
    normaliser = pickle.load(open("normaliser.pkl", "rb"))
    track_features_normalised = normaliser.transform(track_features)
    return track_features_normalised


def predict(model, track_id):
    normalised_track_features = normalise(track_id)
    prediction_array = model.predict(normalised_track_features).asformat("array")[0]
    probabilities_array = model.predict_proba(normalised_track_features).asformat("array")[0]
    genres_list = [i for i, val in enumerate(prediction_array) if val == 1]
    prediction = [GENRE_LIST[genre_idx] for genre_idx in genres_list]
    probabilities = {genre: probabilities_array[index] for index, genre in GENRE_LIST.items()}
    return (prediction, probabilities)
