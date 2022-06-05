import pandas as pd
import numpy as np
import pickle
from os import getcwd
from sklearn.model_selection import train_test_split
from skmultilearn.problem_transform import LabelPowerset
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

GENRES = ['classical', 'country', 'edm', 'hip-hop', 'jazz', 'pop', 'rap', 'rnb', 'rock']

# Drop artists and name so only feature values are stored in dataset
tracks = pd.read_pickle(getcwd() + "/data/spotify_dataset_all.pkl")
cleaned_tracks = tracks.drop(['artists', 'name'], axis=1)

# Drop genre indicators and normalise all values
normaliser = MinMaxScaler()
cleaned_tracks_no_genres = cleaned_tracks.drop(GENRES, axis=1)
normalised_tracks = normaliser.fit_transform(cleaned_tracks_no_genres)
cleaned_tracks_no_genres = pd.DataFrame(normalised_tracks, columns=cleaned_tracks_no_genres.columns).set_index(cleaned_tracks_no_genres.index)
# Merge genre values back to normalised data
cleaned_tracks = pd.merge(cleaned_tracks_no_genres, cleaned_tracks[GENRES], left_index=True, right_index=True)

# Serialise the fitted normaliser so it can be used again for new data
pickle.dump(normaliser, open("normaliser.pkl", "wb"))

# Sample 420 tracks from each genre
resampled_df = pd.DataFrame()
for genre in GENRES:
    genre_df = cleaned_tracks.loc[cleaned_tracks[genre] == 1].sample(n=420)
    resampled_df = pd.concat([resampled_df, genre_df])
# Drop any tracks that already exist in the dataframe
resampled_df.drop_duplicates(inplace=True)

# Set variables; X will be the audio features and y will be the labels
X = resampled_df.drop(GENRES, axis=1).to_numpy()
y = resampled_df.loc[:, GENRES].to_numpy()

# Split data 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Label Powerset classifier with Logistic Regression base
clf = LabelPowerset(LogisticRegression(max_iter=400))
clf.fit(X_train, y_train)
# Serialise the model to use for predictions
pickle.dump(clf, open("model.pkl", "wb"))
