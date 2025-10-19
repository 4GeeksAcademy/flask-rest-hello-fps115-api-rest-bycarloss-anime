from flask import Blueprint, jsonify, request
from sqlalchemy import desc
from models import db, Anime, Episode
from utils import APIException, paginate_query

anime_bp = Blueprint("anime_bp", __name__)

@anime_bp.get("/anime")
def list_anime():
    q = request.args.get("q", type=str)
    a_type = request.args.get("type", type=str)
    year = request.args.get("year", type=int)
    page = request.args.get("page")
    limit = request.args.get("limit")

    query = Anime.query
    if q:
        query = query.filter(Anime.title.ilike(f"%{q}%"))
    if a_type:
        query = query.filter(Anime.type == a_type)
    if year:
        query = query.filter(Anime.year == year)

    query = query.order_by(desc(Anime.score), desc(Anime.year), Anime.title.asc())
    items, meta = paginate_query(query, page, limit)
    return jsonify({**meta, "results": [a.serialize() for a in items]}), 200

@anime_bp.get("/anime/<int:anime_id>")
def get_anime(anime_id: int):
    anime = Anime.query.get(anime_id)
    if not anime:
        raise APIException("Anime not found", status_code=404)
    return jsonify(anime.serialize()), 200

@anime_bp.get("/anime/<int:anime_id>/episodes")
def list_anime_episodes(anime_id: int):
    exists = db.session.query(Anime.id).filter_by(id=anime_id).first()
    if not exists:
        raise APIException("Anime not found", status_code=404)
    page = request.args.get("page")
    limit = request.args.get("limit")
    query = Episode.query.filter_by(anime_id=anime_id).order_by(Episode.ep_number.asc().nullslast(), Episode.id.asc())
    items, meta = paginate_query(query, page, limit)
    return jsonify({**meta, "results": [e.serialize() for e in items]}), 200
