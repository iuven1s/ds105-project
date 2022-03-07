import os
import json
import requests

# Set CLIENT_ID and CLIENT_SECRET as environment variables
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"


def get_access_token(url, client_id, client_secret):
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
        }
    auth_resp = requests.post(url, params)
    auth_resp_json = auth_resp.json()
    return auth_resp_json['access_token']


def main():
    access_token = get_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)
    print(access_token)


if __name__ == "__main__":
    main()
