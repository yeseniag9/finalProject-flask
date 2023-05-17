from flask import Blueprint, request, jsonify, render_template 
from helpers import token_required
from models import db, User, Sneaker, sneaker_schema, sneakers_schema 

api = Blueprint('api', __name__, url_prefix='/api') 

@api.route('/sneakers', methods = ['POST']) 
@token_required 
def create_sneaker(current_user_token):
    name = request.json['name']
    date = request.json['date'] 
    color = request.json['color']
    size = request.json['size']
    user_token = current_user_token.token

    print(f'Token: {current_user_token.token}')

    sneaker = Sneaker(name, date, color, size, user_token = user_token)

    db.session.add(sneaker)
    db.session.commit() 

    response = sneaker_schema.dump(sneaker)
    return jsonify(response) 

@api.route('/sneakers', methods = ['GET'])
@token_required
def get_sneaker(current_user_token):
    a_user = current_user_token.token
    sneakers = Sneaker.query.filter_by(user_token = a_user).all()
    response = sneakers_schema.dump(sneakers)
    return jsonify(response)

@api.route('/sneakers/<id>', methods = ['GET'])
@token_required
def get_single_sneaker(current_user_token, id): 
    sneaker = Sneaker.query.get(id)
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

@api.route('/sneakers/<id>', methods = ['POST', 'PUT']) 
@token_required
def update_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    sneaker.name = request.json['name']
    sneaker.date = request.json['date']
    sneaker.way = request.json['color']
    sneaker.size = request.json['size']
    sneaker.user_token = current_user_token.token

    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

@api.route('/sneakers/<id>', methods = ['DELETE'])
@token_required
def delete_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    db.session.delete(sneaker)
    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)