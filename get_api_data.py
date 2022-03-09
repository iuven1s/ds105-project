import os
import requests

# Set CLIENT_ID and CLIENT_SECRET as environment variables
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"


def get_access_token(url, client_id, client_secret):
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(url, params)
        response.raise_for_status()
        access_token_header = {
            "Authorization": f"Bearer {response.json()['access_token']}"
        }
        return access_token_header
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) from error


def multiple_audio_features_endpoint(ids, headers):
    try:
        response = requests.get(
            BASE_URL + f"audio-features?ids={ids}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) from error


def playlist_tracks_endpoint(id, headers, **query_args):
    if query_args is not None:
        args = [f"{param}={val}" for param, val in query_args.items()]
        query_str = "?" + "&".join(args)
    else:
        query_str = None

    try:
        response = requests.get(
            BASE_URL + f"playlists/{id}/tracks" + query_str,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) from error


def general_endpoint(uri, headers):
    try:
        response = requests.get(
            uri,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        raise SystemError(error) from error