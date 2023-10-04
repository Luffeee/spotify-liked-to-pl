import spotipy
import os

from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                               client_secret=os.environ["CLIENT_SECRET"],
                                               redirect_uri="http://127.0.0.1:8080/",
                                               scope="playlist-modify-public playlist-modify-private user-library-read"))

current_user = sp.current_user()
username = current_user['id'] if current_user else None

if username:
    # You can rename your playlist (optional)
    playlist_name = 'My New Playlist'

    new_playlist = sp.user_playlist_create(
        user=username, name=playlist_name, public=False)

    offset = 0
    limit = 50  # Do not change this so you don't get rate limited!
    all_liked_songs = []

    while True:
        liked_songs = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not liked_songs['items']:
            break
        all_liked_songs.extend(liked_songs['items'])
        offset += limit

    # Extract track URIs from the liked songs
    track_uris = [track['track']['uri'] for track in all_liked_songs]

    # Add all the liked songs to the new playlist in batches
    for i in range(0, len(track_uris), 50):
        batch_tracks = track_uris[i:i + 50]
        sp.user_playlist_add_tracks(
            user=username, playlist_id=new_playlist['id'], tracks=batch_tracks)

    print(
        f'Created playlist "{playlist_name}" and added {len(track_uris)} liked songs to it.')
else:
    print('Unable to fetch your Spotify username.')
