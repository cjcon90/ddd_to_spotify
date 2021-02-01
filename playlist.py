import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re


def set_up_spotify():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            redirect_uri="http://example.com/",
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            show_dialog=True,
            cache_path="token.txt"
        )
    )


class PlaylistMachine:
    def __init__(self, scraped_songs):
        self.scraped_songs = scraped_songs.song_list
        self.title = scraped_songs.title
        self.sp = set_up_spotify()
        self.user_id = self.sp.current_user()['id']
        self.song_uris = self._get_track_uris_()
        self._create_playlist_()

    def _get_track_uris_(self):
        print("Finding songs in spotify...")
        arr = []
        for song in self.scraped_songs:
            title = song[0]
            # Remove any (YYYY) from before or after the artist name
            artist_minus_year = re.sub('[(][0-9]{2,4}[)]', '', song[1])
            # remove any Â or &nbsp; characters from the artist name
            artist_minus_whitespace = re.sub('[Â]', '', artist_minus_year)
            # If there are multiple artists listed for the same song (as in cover performances)...
            # ...only search for the first artist
            artist = artist_minus_whitespace.strip().split('/')[0]
            new_song = self.sp.search(q=f"{title} {artist}", type="track")
            try:
                uri = new_song["tracks"]["items"][0]["uri"]
                arr.append(uri)
            except IndexError:
                print(f"Couldn't find '{title}' by {artist} in Spotify. Skipped.")
        print(f"\n{len(arr)} of {len(self.scraped_songs)} songs found.")
        return arr

    def _create_playlist_(self):

        # Split the song_uri list into maximum chunks of 100 songs
        # As this is the max amount of songs to add at any one time
        track_list = [self.song_uris[i * 100:(i + 1) * 100] for i in range((len(self.song_uris) + 100 - 1) // 100)]

        print(f"Creating playlist {self.title} for user {self.user_id}...")

        # Create a new playlist in the spotify account
        new_playlist = self.sp.user_playlist_create(self.user_id,
                                                    f"{self.title} - DigitalDreamDoor.com",
                                                    public=True,
                                                    collaborative=None,
                                                    description=f"A playlist built from the music list '{self.title}'"
                                                                f"on digitaldreamdoor.com")

        playlist_id = new_playlist['id']
        print("Adding songs to playlist...\n")
        # For each set of max 100 songs in the list of tracks, add the songs to the newly created playlist
        for track_set in track_list:
            self.sp.playlist_add_items(playlist_id, track_set)

        print(f"Process complete! Listen to your new playlist at: {new_playlist['external_urls']['spotify']}")
