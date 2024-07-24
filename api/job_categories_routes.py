from flask import Flask, request, jsonify, Blueprint

from api.connection import db

from api.models import Category, row_to_dict

category_blueprint = Blueprint('category_blueprint', __name__)


# add /categories to the blueprint


@category_blueprint.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([row_to_dict(category) for category in Category.query.all()])


@category_blueprint.route('/categories', methods=['POST'])
def create_category():
    print("Request: ", request.json)
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify(row_to_dict(category)), 201


@category_blueprint.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(row_to_dict(category)), 200


@category_blueprint.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    data = request.json
    category.name = data['name']
    db.session.commit()
    return jsonify(row_to_dict(category)), 200


@category_blueprint.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(row_to_dict(category)), 200
