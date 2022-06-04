import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from skmultilearn.adapt import MLARAM

GENRES = ['classical', 'country', 'edm', 'hip-hop', 'jazz', 'pop', 'rap', 'rnb', 'rock']

tracks = pd.read_pickle("spotify_dataset_all.pkl")
cleaned_tracks = tracks.drop(['artists', 'name'], axis=1)

normalised_vals = cleaned_tracks.drop(GENRES, axis=1)
normalised_vals = (normalised_vals - normalised_vals.min())/(normalised_vals.max() - normalised_vals.min())
cleaned_tracks = pd.merge(normalised_vals, cleaned_tracks[GENRES], left_index=True, right_index=True)

resampled_df = pd.DataFrame()

for genre in GENRES:
    genre_df = cleaned_tracks.loc[cleaned_tracks[genre] == 1].sample(n=420)
    resampled_df = pd.concat([resampled_df, genre_df])

X = resampled_df.drop(GENRES, axis=1).to_numpy()
y = resampled_df.loc[:, GENRES].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


clf = MLARAM(threshold=0.02, vigilance=0.94).fit(X_train, y_train)

pickle.dump(clf, open("model.pkl", "wb"))