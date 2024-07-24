from flask import Flask, request, jsonify, Blueprint

from api.connection import db

from api.models import Category

category_blueprint = Blueprint('category_blueprint', __name__)


@category_blueprint.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([category.to_dict() for category in Category.query.all()])


@category_blueprint.route('/categories', methods=['POST'])
def create_category():
    print("Request: ", request.json)
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201
