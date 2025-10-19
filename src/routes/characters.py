from flask import Blueprint, jsonify, request
from models import Character
from utils import APIException, paginate_query

characters_bp = Blueprint("characters_bp", __name__)

@characters_bp.get("/characters")
def list_characters():
    q = request.args.get("q", type=str)
    page = request.args.get("page")
    limit = request.args.get("limit")

    query = Character.query
    if q:
        query = query.filter(Character.name.ilike(f"%{q}%"))
    items, meta = paginate_query(query, page, limit)
    return jsonify({**meta, "results": [c.serialize() for c in items]}), 200

@characters_bp.get("/characters/<int:character_id>")
def get_character(character_id: int):
    character = Character.query.get(character_id)
    if not character:
        raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200
