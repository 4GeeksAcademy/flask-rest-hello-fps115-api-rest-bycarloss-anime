import time
from models import db, Anime, Character, Episode
from services.jikan import get_top_anime, get_anime_detail, get_anime_characters, get_anime_episodes
from app import app

def seed_from_jikan(limit=5):
    with app.app_context():
        top = get_top_anime(limit)
        for item in top.get("data", []):
            mal_id = item["mal_id"]
            detail = get_anime_detail(mal_id).get("data", {})
            anime = Anime.query.filter_by(mal_id=mal_id).first()
            if not anime:
                anime = Anime(mal_id=mal_id, title=detail.get("title"))
            anime.cover_image_url = detail.get("images", {}).get("jpg", {}).get("image_url")
            anime.type = detail.get("type")
            anime.year = detail.get("year")
            anime.score = detail.get("score")
            anime.status = detail.get("status")
            anime.synopsis = detail.get("synopsis")
            db.session.add(anime)
            db.session.commit()
            chars = get_anime_characters(mal_id).get("data", [])
            for c in chars:
                cid = c.get("character", {}).get("mal_id")
                if not cid:
                    continue
                ch = Character.query.filter_by(mal_id=cid).first()
                if not ch:
                    ch = Character(mal_id=cid, name=c["character"].get("name"))
                ch.image_url = c["character"]["images"]["jpg"]["image_url"]
                db.session.add(ch)
            db.session.commit()
            eps = get_anime_episodes(mal_id).get("data", [])
            for e in eps:
                ep = Episode.query.filter_by(anime_id=anime.id, ep_number=e.get("mal_id") or e.get("episode_id")).first()
                if not ep:
                    ep = Episode(anime_id=anime.id, ep_number=e.get("mal_id") or e.get("episode_id"))
                ep.title = e.get("title") or e.get("title_japanese")
                ep.aired_date = e.get("aired") or e.get("aired_date")
                ep.forum_url = e.get("forum_url")
                db.session.add(ep)
            db.session.commit()
            time.sleep(1)
