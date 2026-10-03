"""
Spotify client wrapper — handles OAuth and all Spotify Web API calls.
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SCOPES = " ".join([
    # Playback
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    # Playlists
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
    # Library
    "user-library-read",
    "user-library-modify",
    # History
    "user-read-recently-played",
    "user-top-read",
    "user-read-playback-position",
])


def get_client() -> spotipy.Spotify:
    """Return an authenticated Spotify client using env-var credentials."""
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

    if not client_id or not client_secret:
        raise EnvironmentError(
            "SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set as environment variables."
        )

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SCOPES,
        open_browser=True,
        cache_path=os.path.expanduser("~/.sayos_spotify_mcp_token"),
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def _track_summary(track: dict) -> dict:
    """Return a compact track summary."""
    if not track:
        return {}
    artists = ", ".join(a["name"] for a in track.get("artists", []))
    return {
        "id": track["id"],
        "name": track["name"],
        "artist": artists,
        "album": track.get("album", {}).get("name", ""),
        "duration_ms": track.get("duration_ms", 0),
        "uri": track.get("uri", ""),
        "url": track.get("external_urls", {}).get("spotify", ""),
    }


def _playlist_summary(pl: dict) -> dict:
    if not pl:
        return {}
    return {
        "id": pl["id"],
        "name": pl["name"],
        "owner": pl.get("owner", {}).get("display_name", ""),
        "tracks_total": pl.get("tracks", {}).get("total", 0),
        "public": pl.get("public", None),
        "uri": pl.get("uri", ""),
        "url": pl.get("external_urls", {}).get("spotify", ""),
    }
