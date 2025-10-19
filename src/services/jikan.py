import os, requests

API = os.getenv("JIKAN_API_URL", "https://api.jikan.moe/v4")

def build_url(path, params=None):
    url = f"{API}{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        if query:
            url += f"?{query}"
    return url

def get_json(path, params=None):
    res = requests.get(build_url(path, params or {}))
    res.raise_for_status()
    return res.json()

def get_top_anime(limit=10):
    return get_json("/top/anime", {"limit": limit})

def get_anime_detail(mal_id):
    return get_json(f"/anime/{mal_id}")

def get_anime_characters(mal_id):
    return get_json(f"/anime/{mal_id}/characters")

def get_anime_episodes(mal_id, page=1):
    return get_json(f"/anime/{mal_id}/episodes", {"page": page})
