import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="your_client_id",
                                               client_secret="your_client_secret",
                                               redirect_uri="your_redirect_uri",
                                               scope="playlist-modify-private"))

class SpotifyPlaylistManager(tk.Tk):
    """
    SpotifyPlaylistManager class for managing Spotify playlists through a GUI.
    """

    def __init__(self):
        """
        Initialize the application window and UI elements.
        """
        super().__init__()
        self.title("Spotify Playlist Manager")

        # Create UI elements
        self.playlist_label = ttk.Label(self, text="Your Playlists:")
        self.playlist_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.playlist_combobox = ttk.Combobox(self, width=40)
        self.playlist_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.sort_label = ttk.Label(self, text="Sort By:")
        self.sort_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.sort_combobox = ttk.Combobox(self, values=["Name", "Artist", "Album", "Release Date", "Popularity"],
                                          width=20)
        self.sort_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.sort_combobox.current(0)

        self.sort_button = ttk.Button(self, text="Sort Playlist", command=self.sort_playlist)
        self.sort_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Load user playlists
        self.load_user_playlists()

    def load_user_playlists(self):
        """
        Retrieve and populate the user's playlists into the combobox.
        """
        playlists = sp.current_user_playlists()
        self.playlist_combobox["values"] = [playlist["name"] for playlist in playlists["items"]]
        if len(playlists["items"]) > 0:
            self.playlist_combobox.current(0)

    def sort_playlist(self):
        """
        Sort the selected playlist according to the chosen sorting option.
        """
        playlist_name = self.playlist_combobox.get()
        sort_option = self.sort_combobox.get()

        # Get playlist ID
        playlists = sp.current_user_playlists()
        playlist_id = None
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                playlist_id = playlist["id"]
                break

        if not playlist_id:
            self.status_label.config(text="Error: Playlist not found.")
            return

        # Sort playlist
        if sort_option == "Name":
            sorted_tracks = sort_playlist_by_name(playlist_id)
        elif sort_option == "Artist":
            sorted_tracks = sort_playlist_by_artist(playlist_id)
        elif sort_option == "Album":
            sorted_tracks = sort_playlist_by_album(playlist_id)
        elif sort_option == "Release Date":
            sorted_tracks = sort_playlist_by_release_date(playlist_id)
        elif sort_option == "Popularity":
            sorted_tracks = sort_playlist_by_popularity(playlist_id)
        else:
            self.status_label.config(text="Error: Invalid sort option.")
            return

        # Update playlist with sorted tracks
        track_uris = [track["uri"] for track in sorted_tracks]
        sp.playlist_replace_items(playlist_id, track_uris)
        self.status_label.config(text="Playlist sorted successfully.")

def sort_playlist_by_name(playlist_id):
    """
    Sort playlist tracks by name.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"] for item in results["items"]]
    sorted_tracks = sorted(tracks, key=lambda x: x["name"])
    return sorted_tracks

def sort_playlist_by_artist(playlist_id):
    """
    Sort playlist tracks by artist.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"] for item in results["items"]]
    sorted_tracks = sorted(tracks, key=lambda x: x["artists"][0]["name"])
    return sorted_tracks

def sort_playlist_by_album(playlist_id):
    """
    Sort playlist tracks by album.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"] for item in results["items"]]
    sorted_tracks = sorted(tracks, key=lambda x: x["album"]["name"])
    return sorted_tracks

def sort_playlist_by_release_date(playlist_id):
    """
    Sort playlist tracks by release date.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"] for item in results["items"]]
    sorted_tracks = sorted(tracks, key=lambda x: x["album"]["release_date"])
    return sorted_tracks

def sort_playlist_by_popularity(playlist_id):
    """
    Sort playlist tracks by popularity.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"] for item in results["items"]]
    sorted_tracks = sorted(tracks, key=lambda x: x["popularity"], reverse=True)
    return sorted_tracks

if __name__ == "__main__":
    app = SpotifyPlaylistManager()
    app.mainloop()
