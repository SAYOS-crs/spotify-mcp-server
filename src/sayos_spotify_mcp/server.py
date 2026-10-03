"""
sayos-spotify-mcp — MCP server entry point.

All Spotify tools are registered here using FastMCP.
"""

from mcp.server.fastmcp import FastMCP
from . import client as sp_client

mcp = FastMCP(
    name="sayos-spotify-mcp",
    version="1.0.0",
    description="Control Spotify from any MCP-compatible AI — search, play, manage playlists, queue tracks, and more.",
)

# ──────────────────────────────────────────────
# PLAYBACK TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def get_current_track() -> dict:
    """Get the currently playing track on Spotify, including title, artist, album, and progress."""
    sp = sp_client.get_client()
    data = sp.current_playback()
    if not data or not data.get("item"):
        return {"status": "nothing_playing"}
    track = data["item"]
    progress_ms = data.get("progress_ms", 0)
    duration_ms = track.get("duration_ms", 1)
    summary = sp_client._track_summary(track)
    summary["is_playing"] = data.get("is_playing", False)
    summary["progress_ms"] = progress_ms
    summary["progress_pct"] = round(progress_ms / duration_ms * 100, 1)
    summary["device"] = data.get("device", {}).get("name", "unknown")
    return summary


@mcp.tool()
def play_track(track_id: str) -> str:
    """
    Start playing a specific track by its Spotify track ID or URI.

    Args:
        track_id: Spotify track ID (e.g. '4iV5W9uYEdYUVa79Axb7Rh') or full URI.
    """
    sp = sp_client.get_client()
    uri = track_id if track_id.startswith("spotify:") else f"spotify:track:{track_id}"
    sp.start_playback(uris=[uri])
    return f"Now playing track: {track_id}"


@mcp.tool()
def resume_playback() -> str:
    """Resume the current paused playback on Spotify."""
    sp = sp_client.get_client()
    sp.start_playback()
    return "Playback resumed."


@mcp.tool()
def pause_playback() -> str:
    """Pause the current Spotify playback."""
    sp = sp_client.get_client()
    sp.pause_playback()
    return "Playback paused."


@mcp.tool()
def skip_to_next() -> str:
    """Skip to the next track in the Spotify queue."""
    sp = sp_client.get_client()
    sp.next_track()
    return "Skipped to next track."


@mcp.tool()
def skip_to_previous() -> str:
    """Go back to the previous track on Spotify."""
    sp = sp_client.get_client()
    sp.previous_track()
    return "Went back to previous track."


@mcp.tool()
def set_volume(volume_percent: int) -> str:
    """
    Set the Spotify playback volume.

    Args:
        volume_percent: Volume level from 0 (mute) to 100 (max).
    """
    volume_percent = max(0, min(100, volume_percent))
    sp = sp_client.get_client()
    sp.volume(volume_percent)
    return f"Volume set to {volume_percent}%."


@mcp.tool()
def set_shuffle(state: bool) -> str:
    """
    Toggle shuffle mode on or off.

    Args:
        state: True to enable shuffle, False to disable.
    """
    sp = sp_client.get_client()
    sp.shuffle(state)
    return f"Shuffle {'enabled' if state else 'disabled'}."


@mcp.tool()
def set_repeat(mode: str) -> str:
    """
    Set the repeat mode for Spotify playback.

    Args:
        mode: One of 'track' (repeat current track), 'context' (repeat playlist/album), or 'off'.
    """
    if mode not in ("track", "context", "off"):
        return "Invalid mode. Use 'track', 'context', or 'off'."
    sp = sp_client.get_client()
    sp.repeat(mode)
    return f"Repeat mode set to '{mode}'."


@mcp.tool()
def get_available_devices() -> list:
    """List all available Spotify Connect devices (speakers, phones, computers, etc.)."""
    sp = sp_client.get_client()
    result = sp.devices()
    devices = result.get("devices", [])
    return [
        {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "is_active": d["is_active"],
            "volume_percent": d.get("volume_percent"),
        }
        for d in devices
    ]


@mcp.tool()
def transfer_playback(device_id: str) -> str:
    """
    Transfer playback to a different Spotify Connect device.

    Args:
        device_id: The device ID to transfer playback to (from get_available_devices).
    """
    sp = sp_client.get_client()
    sp.transfer_playback(device_id, force_play=True)
    return f"Playback transferred to device: {device_id}"


# ──────────────────────────────────────────────
# SEARCH TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def search_tracks(query: str, limit: int = 10) -> list:
    """
    Search for tracks on Spotify.

    Args:
        query: Search query (e.g. 'Peachy Keen Tusks').
        limit: Number of results to return (1–50, default 10).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.search(q=query, type="track", limit=limit)
    tracks = results.get("tracks", {}).get("items", [])
    return [sp_client._track_summary(t) for t in tracks]


@mcp.tool()
def search_artists(query: str, limit: int = 10) -> list:
    """
    Search for artists on Spotify.

    Args:
        query: Artist name to search.
        limit: Number of results (1–50, default 10).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.search(q=query, type="artist", limit=limit)
    artists = results.get("artists", {}).get("items", [])
    return [
        {
            "id": a["id"],
            "name": a["name"],
            "genres": a.get("genres", []),
            "followers": a.get("followers", {}).get("total", 0),
            "uri": a.get("uri", ""),
            "url": a.get("external_urls", {}).get("spotify", ""),
        }
        for a in artists
    ]


@mcp.tool()
def search_playlists(query: str, limit: int = 10) -> list:
    """
    Search for playlists on Spotify.

    Args:
        query: Playlist name or keyword.
        limit: Number of results (1–50, default 10).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.search(q=query, type="playlist", limit=limit)
    playlists = results.get("playlists", {}).get("items", [])
    return [sp_client._playlist_summary(p) for p in playlists if p]


@mcp.tool()
def search_albums(query: str, limit: int = 10) -> list:
    """
    Search for albums on Spotify.

    Args:
        query: Album name or keyword.
        limit: Number of results (1–50, default 10).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.search(q=query, type="album", limit=limit)
    albums = results.get("albums", {}).get("items", [])
    return [
        {
            "id": a["id"],
            "name": a["name"],
            "artist": ", ".join(ar["name"] for ar in a.get("artists", [])),
            "release_date": a.get("release_date", ""),
            "total_tracks": a.get("total_tracks", 0),
            "uri": a.get("uri", ""),
            "url": a.get("external_urls", {}).get("spotify", ""),
        }
        for a in albums
    ]


# ──────────────────────────────────────────────
# QUEUE TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def get_queue() -> dict:
    """Get the current Spotify playback queue (currently playing + up next)."""
    sp = sp_client.get_client()
    data = sp.queue()
    currently_playing = data.get("currently_playing")
    queue_tracks = data.get("queue", [])
    return {
        "currently_playing": sp_client._track_summary(currently_playing) if currently_playing else None,
        "queue": [sp_client._track_summary(t) for t in queue_tracks[:20]],
    }


@mcp.tool()
def add_to_queue(track_id: str) -> str:
    """
    Add a track to the end of the Spotify playback queue.

    Args:
        track_id: Spotify track ID or full URI.
    """
    sp = sp_client.get_client()
    uri = track_id if track_id.startswith("spotify:") else f"spotify:track:{track_id}"
    sp.add_to_queue(uri)
    return f"Track added to queue: {track_id}"


# ──────────────────────────────────────────────
# PLAYLIST TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def get_my_playlists(limit: int = 20) -> list:
    """
    Get the current user's Spotify playlists.

    Args:
        limit: Number of playlists to return (1–50, default 20).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.current_user_playlists(limit=limit)
    return [sp_client._playlist_summary(p) for p in results.get("items", []) if p]


@mcp.tool()
def get_playlist_tracks(playlist_id: str, limit: int = 50) -> list:
    """
    Get tracks from a specific playlist.

    Args:
        playlist_id: Spotify playlist ID.
        limit: Number of tracks to return (1–100, default 50).
    """
    sp = sp_client.get_client()
    limit = max(1, min(100, limit))
    results = sp.playlist_tracks(playlist_id, limit=limit)
    items = results.get("items", [])
    return [sp_client._track_summary(item["track"]) for item in items if item.get("track")]


@mcp.tool()
def create_playlist(name: str, description: str = "", public: bool = False) -> dict:
    """
    Create a new Spotify playlist for the current user.

    Args:
        name: Name of the new playlist.
        description: Optional description for the playlist.
        public: Whether the playlist should be public (default False = private).
    """
    sp = sp_client.get_client()
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        description=description,
    )
    return sp_client._playlist_summary(playlist)


@mcp.tool()
def add_tracks_to_playlist(playlist_id: str, track_ids: list) -> str:
    """
    Add one or more tracks to a Spotify playlist.

    Args:
        playlist_id: Target playlist ID.
        track_ids: List of track IDs or URIs to add.
    """
    sp = sp_client.get_client()
    uris = [t if t.startswith("spotify:") else f"spotify:track:{t}" for t in track_ids]
    sp.playlist_add_items(playlist_id, uris)
    return f"Added {len(uris)} track(s) to playlist {playlist_id}."


@mcp.tool()
def remove_tracks_from_playlist(playlist_id: str, track_ids: list) -> str:
    """
    Remove one or more tracks from a Spotify playlist.

    Args:
        playlist_id: Target playlist ID.
        track_ids: List of track IDs or URIs to remove.
    """
    sp = sp_client.get_client()
    uris = [t if t.startswith("spotify:") else f"spotify:track:{t}" for t in track_ids]
    sp.playlist_remove_all_occurrences_of_items(playlist_id, uris)
    return f"Removed {len(uris)} track(s) from playlist {playlist_id}."


@mcp.tool()
def play_playlist(playlist_id: str) -> str:
    """
    Start playing a Spotify playlist from the beginning.

    Args:
        playlist_id: Spotify playlist ID or URI.
    """
    sp = sp_client.get_client()
    uri = playlist_id if playlist_id.startswith("spotify:") else f"spotify:playlist:{playlist_id}"
    sp.start_playback(context_uri=uri)
    return f"Now playing playlist: {playlist_id}"


# ──────────────────────────────────────────────
# LIBRARY TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def get_liked_songs(limit: int = 20) -> list:
    """
    Get tracks from the current user's Liked Songs library.

    Args:
        limit: Number of tracks to return (1–50, default 20).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.current_user_saved_tracks(limit=limit)
    return [sp_client._track_summary(item["track"]) for item in results.get("items", []) if item.get("track")]


@mcp.tool()
def like_track(track_id: str) -> str:
    """
    Add a track to the current user's Liked Songs.

    Args:
        track_id: Spotify track ID to like.
    """
    sp = sp_client.get_client()
    track_id = track_id.split(":")[-1]  # strip URI prefix if provided
    sp.current_user_saved_tracks_add([track_id])
    return f"Track {track_id} added to Liked Songs."


@mcp.tool()
def unlike_track(track_id: str) -> str:
    """
    Remove a track from the current user's Liked Songs.

    Args:
        track_id: Spotify track ID to remove.
    """
    sp = sp_client.get_client()
    track_id = track_id.split(":")[-1]
    sp.current_user_saved_tracks_delete([track_id])
    return f"Track {track_id} removed from Liked Songs."


@mcp.tool()
def get_top_tracks(time_range: str = "medium_term", limit: int = 20) -> list:
    """
    Get the current user's top tracks on Spotify.

    Args:
        time_range: One of 'short_term' (4 weeks), 'medium_term' (6 months), 'long_term' (all time).
        limit: Number of results (1–50, default 20).
    """
    if time_range not in ("short_term", "medium_term", "long_term"):
        return [{"error": "time_range must be 'short_term', 'medium_term', or 'long_term'"}]
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    return [sp_client._track_summary(t) for t in results.get("items", [])]


@mcp.tool()
def get_recently_played(limit: int = 20) -> list:
    """
    Get the current user's recently played tracks on Spotify.

    Args:
        limit: Number of results (1–50, default 20).
    """
    sp = sp_client.get_client()
    limit = max(1, min(50, limit))
    results = sp.current_user_recently_played(limit=limit)
    return [sp_client._track_summary(item["track"]) for item in results.get("items", []) if item.get("track")]


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
