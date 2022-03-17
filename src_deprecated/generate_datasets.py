import pandas as pd
import numpy as np
from os.path import exists
from datetime import datetime
from api_functions import *

PLAYLIST_IDS = {
    "classical": "3HYK6ri0GkvRcM6GkKh0hJ",
    "country": "4mijVkpSXJziPiOrK7YX4M",
    "edm": "3pDxuMpz94eDs7WFqudTbZ",
    "hip-hop": "6MXkE0uYF4XwU4VTtyrpfP",
    "jazz": "5EyFMotmvSfDAZ4hSdKrbx",
    "pop": "6gS3HhOiI17QNojjPuPzqc",
    "rap": "6s5MoZzR70Qef7x4bVxDO1",
    "rnb": "1rLnwJimWCmjp3f0mEbnkY",
    "rock": "7dowgSWOmvdpwNkGFMUs6e"
}


def get_playlist_data(playlist_id, access_token):
    # First call to get playlist information
    playlist_response = playlist_tracks_endpoint(playlist_id, access_token)

    # If playlist has more than 100 songs, more calls will be necessary
    all_responses = [playlist_response]
    next_page = playlist_response['next']
    while next_page is not None:
        offset_response = general_endpoint(next_page, access_token)
        all_responses.append(offset_response)
        next_page = offset_response['next']
    return all_responses


def create_playlist_df(playlist_responses, genre):
    cleaned_tracks = {}
    for response in playlist_responses:
        for track in response['items']:
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artists = [artist['name'] for artist in track['track']['artists']]
            cleaned_tracks[track_id] = {'artists': track_artists, 'name': track_name, 'genre': genre}
    all_tracks_df = pd.DataFrame.from_dict(cleaned_tracks, orient='index')
    return all_tracks_df


def prepare_ids_for_query(ids, max_len=100):
    track_ids = np.array(ids)
    split_ids = []
    # If there are more than 100 tracks in the playlist
    while len(track_ids) > max_len:
        # Create a string of comma-delimited ids and add this to a list
        split_ids.append(",".join(track_ids[:max_len]))
        # Move on to next section of ids
        track_ids = np.delete(track_ids, np.s_[:max_len])
    # Add any remaining tracks (or add all tracks if number of tracks are sub 100)
    split_ids.append(",".join(track_ids))
    return split_ids


def get_release_date(data):
    try:
        return pd.to_datetime(data['album']['release_date']).year
    except:
        return pd.NA


def create_track_info_df(track_info_list):
    all_tracks_info_df = pd.DataFrame()
    # For each length-50 grouping of tracks
    for tracks in track_info_list:
        tracks_info = tracks['tracks']
        tracks_ids = [data['id'] for data in tracks_info]
        tracks_release_year = [get_release_date(data) for data in tracks_info]
        tracks_popularity = [data['popularity'] for data in tracks_info]
        tracks_info_df = pd.DataFrame({'release_year': tracks_release_year, 'popularity': tracks_popularity}, index=tracks_ids)
        all_tracks_info_df = pd.concat([all_tracks_info_df, tracks_info_df])
    return all_tracks_info_df


def create_audio_features_df(audio_features_list):
    all_audio_features_df = pd.DataFrame()
    # For each length-100 grouping of tracks
    for tracks_features in audio_features_list:
        audios_features = tracks_features['audio_features']
        tracks_ids = [data['id'] for data in audios_features]
        features_df = pd.DataFrame(audios_features, index=tracks_ids)
        # Drop irrelevant columns
        features_df.drop(['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1, inplace=True)
        all_audio_features_df = pd.concat([all_audio_features_df, features_df])
    return all_audio_features_df


def main():
    access_token_header = get_access_token(CLIENT_ID, CLIENT_SECRET)

    for playlist_name, playlist_id in PLAYLIST_IDS.items():
        playlist_data = get_playlist_data(playlist_id, access_token_header)
        playlist_df = create_playlist_df(playlist_data, playlist_name)

        track_ids = playlist_df.index
        # Max ids is 100 for Audio Features, but 50 for Get Several Tracks
        ids_list_100, ids_list_50 = prepare_ids_for_query(track_ids), prepare_ids_for_query(track_ids, 50)

        all_tracks_info_list = [multiple_tracks_info_endpoint(ids, access_token_header) for ids in ids_list_50]
        all_audio_features_list = [multiple_audio_features_endpoint(ids, access_token_header) for ids in ids_list_100]

        track_info_df = create_track_info_df(all_tracks_info_list)
        audio_features_df = create_audio_features_df(all_audio_features_list)

        info_with_features_df = pd.merge(track_info_df, audio_features_df, left_index=True, right_index=True)
        tracks_df = pd.merge(playlist_df, info_with_features_df, left_index=True, right_index=True)
        tracks_df.dropna(inplace=True)
        tracks_df.to_pickle(f"data_deprecated/spotify_dataset_{playlist_name}.pkl")


if __name__ == "__main__":
    main()
