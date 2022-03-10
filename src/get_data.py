import pandas as pd
import numpy as np
from src.api_functions import *

PLAYLIST_ID = '6VaNNtZuGdbQ3GMNnhPl9e'


def get_playlist_data(playlist_id, access_token_header):
    # First call to get playlist metadata
    first_response = playlist_tracks_endpoint(
        playlist_id,
        access_token_header
    )
    all_responses = [first_response]
    # If playlist has more than 100 calls, more calls will be necessary
    next_page = first_response['next']
    while next_page is not None:
        offset_response = general_endpoint(
            next_page,
            access_token_header
        )
        all_responses.append(offset_response)
        next_page = offset_response['next']

    return all_responses


def create_track_dataframe(all_track_data):
    cleaned_tracks = {}

    for response in all_track_data:
        for track in response['items']:
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artists = [
                artist['name']
                for artist 
                in track['track']['artists']
            ]
            cleaned_tracks[track_id] = {
                'artists': track_artists,
                'name': track_name
            }
    all_tracks_df = pd.DataFrame.from_dict(cleaned_tracks, orient='index')
    return all_tracks_df


def prepare_ids_for_query(all_tracks_df, max_len=100):
    track_ids = np.array(all_tracks_df.index)
    split_ids = []
    # If there are more than 100 tracks in the playlist
    while len(track_ids) > max_len:
        # Create a string of comma-delimited ids and add this to a list
        split_ids.append(",".join(track_ids[:max_len]))
        # Move on to next section of ids
        track_ids = np.delete(track_ids, np.s_[:max_len])
    # Add any remaining tracks (or all tracks if number of tracks are sub 100)
    split_ids.append(",".join(track_ids))
    return split_ids


def get_features_data(ids_list, access_token_header):
    all_features_list = [
        multiple_audio_features_endpoint(
            ids,
            access_token_header
        )
        for ids
        in ids_list
    ]
    return all_features_list


def create_features_dataframe(all_features_list):
    all_audio_features_df = pd.DataFrame()

    for tracks_data in all_features_list:
        tracks_features = tracks_data['audio_features']
        ids = [data['id'] for data in tracks_features]
        features_df = pd.DataFrame(tracks_features, index=ids)
        # Drop irrelevant columns
        features_df.drop(
            ['type', 'id', 'uri', 'track_href', 'analysis_url'],
            axis=1,
            inplace=True
        )
        all_audio_features_df = pd.concat(
            [all_audio_features_df, features_df]
        )
    return all_audio_features_df


def main():
    access_token_header = get_access_token(CLIENT_ID, CLIENT_SECRET)
    all_tracks_df = create_track_dataframe(
        get_playlist_data(PLAYLIST_ID, access_token_header)
    )
    all_audio_features_df = create_features_dataframe(
        get_features_data(
            prepare_ids_for_query(all_tracks_df),
            access_token_header
        )
    )
    tracks_and_features_df = pd.merge(
        all_tracks_df,
        all_audio_features_df,
        left_index=True,
        right_index=True
    )
    print(tracks_and_features_df)


if __name__ == "__main__":
    main()
