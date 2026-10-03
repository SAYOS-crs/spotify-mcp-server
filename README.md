# sayos-spotify-mcp 🎵

A **full-featured Spotify MCP server** that lets any MCP-compatible AI (Antigravity, Claude, Cursor, etc.) control your Spotify — search tracks, manage playback, create playlists, browse your library, and more.

**Built by [SAYOS-crs](https://github.com/SAYOS-crs)**

---

## ✨ Features

| Category | Tools |
|----------|-------|
| 🎵 **Playback** | Play track, pause, resume, skip next/prev, set volume, shuffle, repeat, transfer device |
| 🔍 **Search** | Search tracks, artists, albums, playlists |
| 📋 **Queue** | View queue, add track to queue |
| 📁 **Playlists** | Get your playlists, get tracks, create playlist, add/remove tracks, play playlist |
| ❤️ **Library** | Liked songs, like/unlike track, top tracks, recently played |
| 📱 **Devices** | List available devices, transfer playback |

**20+ tools total.**

---

## 🚀 Quick Setup

### 1. Install

```bash
pip install sayos-spotify-mcp
```

### 2. Create a Spotify App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click **Create app**
3. Set Redirect URI to: `http://127.0.0.1:8888/callback`
4. Copy your **Client ID** and **Client Secret**

### 3. Add to your MCP config (`~/.gemini/config/mcp_config.json` for Antigravity)

```json
{
  "mcpServers": {
    "spotify": {
      "command": "sayos-spotify-mcp",
      "env": {
        "SPOTIPY_CLIENT_ID": "YOUR_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "SPOTIPY_REDIRECT_URI": "http://localhost:8888/callback"
      }
    }
  }
}
```

### 4. Authorize

On first use, a browser window will open asking you to log in to Spotify and grant access. After that, your token is cached automatically.

---

## 🧠 Works with

- **[Antigravity (AGY)](https://antigravity.google)** — add to `~/.gemini/config/mcp_config.json`
- **[Claude Desktop](https://claude.ai/download)** — add to `claude_desktop_config.json`
- **[Cursor](https://cursor.sh)** — add to `.cursor/mcp.json`
- Any other MCP-compatible client

---

## 🛠 Available Tools

### Playback
| Tool | Description |
|------|-------------|
| `get_current_track` | Get what's currently playing |
| `play_track(track_id)` | Play a specific track by ID |
| `resume_playback` | Resume paused playback |
| `pause_playback` | Pause playback |
| `skip_to_next` | Skip to next track |
| `skip_to_previous` | Go back to previous track |
| `set_volume(volume_percent)` | Set volume 0–100 |
| `set_shuffle(state)` | Enable/disable shuffle |
| `set_repeat(mode)` | Set repeat: `track`, `context`, or `off` |
| `get_available_devices` | List Spotify Connect devices |
| `transfer_playback(device_id)` | Move playback to another device |

### Search
| Tool | Description |
|------|-------------|
| `search_tracks(query, limit)` | Search for tracks |
| `search_artists(query, limit)` | Search for artists |
| `search_albums(query, limit)` | Search for albums |
| `search_playlists(query, limit)` | Search for playlists |

### Queue
| Tool | Description |
|------|-------------|
| `get_queue` | View current queue |
| `add_to_queue(track_id)` | Add a track to the queue |

### Playlists
| Tool | Description |
|------|-------------|
| `get_my_playlists(limit)` | Get your playlists |
| `get_playlist_tracks(playlist_id)` | Get tracks in a playlist |
| `create_playlist(name, description, public)` | Create a new playlist |
| `add_tracks_to_playlist(playlist_id, track_ids)` | Add tracks to a playlist |
| `remove_tracks_from_playlist(playlist_id, track_ids)` | Remove tracks from a playlist |
| `play_playlist(playlist_id)` | Play a playlist |

### Library
| Tool | Description |
|------|-------------|
| `get_liked_songs(limit)` | Get your Liked Songs |
| `like_track(track_id)` | Like a track |
| `unlike_track(track_id)` | Unlike a track |
| `get_top_tracks(time_range, limit)` | Your top tracks |
| `get_recently_played(limit)` | Recently played tracks |

---

## 📋 Requirements

- Python 3.10+
- A Spotify Premium account (required for playback control)
- A Spotify Developer app

---

## 📄 License

MIT © [SAYOS-crs](https://github.com/SAYOS-crs)
