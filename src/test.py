from api_functions import *
import pandas as pd
import numpy as np
from os import getcwd

trk = '7zpMz3am0n83WmDxVqp9GQ'

token = get_access_token(CLIENT_ID, CLIENT_SECRET)

af = general_endpoint(BASE_URL + f'audio-features/{trk}', headers=token)

vs = ['type', 'id', 'uri', 'track_href', 'analysis_url']

for v in vs:
    del af[v]

df = pd.DataFrame(af, index=[trk,])

tracks = pd.read_pickle(getcwd() + "/data/spotify_dataset_all.pkl")
cleaned_tracks = tracks.drop(['artists', 'name'], axis=1)

GENRES = ['classical', 'country', 'edm', 'hip-hop', 'jazz', 'pop', 'rap', 'rnb', 'rock']
normalised_vals = cleaned_tracks.drop(GENRES, axis=1)
normalised_vals = pd.concat([normalised_vals, df])

normalised_vals = (normalised_vals - normalised_vals.min())/(normalised_vals.max() - normalised_vals.min())

normalised_vals.loc['7zpMz3am0n83WmDxVqp9GQ'].drop_duplicates().to_pickle(getcwd() + "/data/test.pkl")