from flask import Blueprint, jsonify
from models import db, User, Anime, Character, Favorite
from utils import APIException, get_current_user_id

users_bp = Blueprint("users_bp", __name__)

@users_bp.get("/users")
def list_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@users_bp.get("/users/favorites")
def list_user_favorites():
    user_id = get_current_user_id()
    favs = Favorite.query.filter_by(user_id=user_id).all()
    results = []
    for f in favs:
        data = f.serialize()
        if f.resource_type == "anime":
            anime = Anime.query.get(f.resource_id)
            if anime:
                data["title"] = anime.title
                data["image"] = anime.cover_image_url
        elif f.resource_type == "character":
            ch = Character.query.get(f.resource_id)
            if ch:
                data["name"] = ch.name
                data["image"] = ch.image_url
        results.append(data)
    return jsonify(results), 200

@users_bp.post("/favorite/anime/<int:anime_id>")
def add_favorite_anime(anime_id: int):
    user_id = get_current_user_id()
    exists = Anime.query.get(anime_id)
    if not exists:
        raise APIException("Anime not found", status_code=404)
    dup = Favorite.query.filter_by(user_id=user_id, resource_type="anime", resource_id=anime_id).first()
    if dup:
        raise APIException("Already in favorites", status_code=409)
    fav = Favorite(user_id=user_id, resource_type="anime", resource_id=anime_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@users_bp.post("/favorite/character/<int:character_id>")
def add_favorite_character(character_id: int):
    user_id = get_current_user_id()
    exists = Character.query.get(character_id)
    if not exists:
        raise APIException("Character not found", status_code=404)
    dup = Favorite.query.filter_by(user_id=user_id, resource_type="character", resource_id=character_id).first()
    if dup:
        raise APIException("Already in favorites", status_code=409)
    fav = Favorite(user_id=user_id, resource_type="character", resource_id=character_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@users_bp.delete("/favorite/anime/<int:anime_id>")
def delete_favorite_anime(anime_id: int):
    user_id = get_current_user_id()
    fav = Favorite.query.filter_by(user_id=user_id, resource_type="anime", resource_id=anime_id).first()
    if not fav:
        raise APIException("Favorite not found", status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return "", 204

@users_bp.delete("/favorite/character/<int:character_id>")
def delete_favorite_character(character_id: int):
    user_id = get_current_user_id()
    fav = Favorite.query.filter_by(user_id=user_id, resource_type="character", resource_id=character_id).first()
    if not fav:
        raise APIException("Favorite not found", status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return "", 204
