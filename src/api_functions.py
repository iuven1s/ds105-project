"""
Helper functions to make requests to Spotify's APIs.
"""

import os
from time import sleep
import requests


# Set CLIENT_ID and CLIENT_SECRET as environment variables
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"


def get_access_token(client_id, client_secret):
    """Gets OAuth2 Bearer token (for making API calls)

    Args:
        client_id (str): Client ID from Spotify
        client_secret (str): Client Secret from Spotify

    Raises:
        SystemExit: Raised if authentication fails

    Returns:
        str: Bearer token
    """
    # Using client credentials flow.
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(AUTH_URL, params)
        response.raise_for_status()
        access_token_header = {
            "Authorization": f"Bearer {response.json()['access_token']}"
        }
        return access_token_header
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) from error


def multiple_audio_features_endpoint(ids, headers):
    """Get Audio Features on multiple tracks (max 100)

    Args:
        ids (str): Comma delimited track ids (e.g. abc,def,ghi)
        headers (str): Header containing bearer token

    Raises:
        SystemExit: Raised if 200 is not received

    Returns:
        dict: Audio features for every track in query
    """
    try:
        response = requests.get(
            BASE_URL + f"audio-features?ids={ids}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 429:
            sleep(int(response.headers['Retry-After']))
            return multiple_audio_features_endpoint(ids, headers)
        raise SystemExit(error) from error


def playlist_tracks_endpoint(playlist_id, headers, **query_args):
    """Gets all tracks from a playlist (max 100). Accepts optional query
    arguments

    Args:
        playlist_id (str): Playlist id
        headers (str): Header containing bearer token

    Raises:
        SystemExit: Raised if 200 is not received

    Returns:
        dict: All tracks in a playlist if there are 100 tracks or less,
        otherwise returns first 100 tracks of a playlist
    """
    if query_args is not None:
        args = [f"{param}={val}" for param, val in query_args.items()]
        query_str = "?" + "&".join(args)
    else:
        query_str = None

    try:
        response = requests.get(
            BASE_URL + f"playlists/{playlist_id}/tracks" + query_str,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 429:
            sleep(int(response.headers['Retry-After']))
            return playlist_tracks_endpoint(playlist_id, headers, **query_args)
        raise SystemExit(error) from error


def search_track_endpoint(query, headers):
    """Searches for tracks based on query. Max output is 20 tracks
    Args:
        query (str): Query for track
        headers (str): Header containing bearer token
    Raises:
        SystemExit: Raised if 200 not received
    Returns:
        dict: 20 or less matching queries
    """
    query = query.replace(" ", "+")
    try:
        response = requests.get(
            BASE_URL + f"search?q={query}&type=track",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 429:
            sleep(int(response.headers['Retry-After']))
            return playlist_tracks_endpoint(query, headers)
        raise SystemExit(error) from error


def general_endpoint(href, headers):
    """General endpoint function. Assumes href is well-formed and complete

    Args:
        href (str): Complete href for Spotify's APIs
        headers (str): Header containing bearer token

    Raises:
        SystemError: Raised if 200 is not received

    Returns:
        dict: Data requested from API
    """
    try:
        response = requests.get(
            href,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 429:
            sleep(int(response.headers['Retry-After']))
            return general_endpoint(href, headers)
        raise SystemExit(error) from error
