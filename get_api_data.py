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


def connect_to_endpoint(request, headers):
    try:
        response = requests.get(BASE_URL + f"{request}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) from error


def main():
    access_token_header = get_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)
    album_tracks_response = connect_to_endpoint(
        'playlists/37i9dQZEVXbNG2KDcFcKOF/tracks',
        access_token_header
    )
    print(album_tracks_response)


if __name__ == "__main__":
    main()
