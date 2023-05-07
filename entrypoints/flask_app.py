from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized
from datetime import datetime
from sqlalchemy import event
from domains.events import ProductCreated, ProductDeleted, ProductUpdated
from service.messagebus import MessageBus
from service.unit_of_work import SQLAlchemyUnitOfWork
from service.handlers import (
    create_user,
    create_product,
    reserve_product,
    create_category
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RREP.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bind SQLAlchemy to MessageBus and create a new UoW instance
message_bus = MessageBus()
uow = SQLAlchemyUnitOfWork(db, message_bus)

# Import entities
from domains.model import Users, Product, Reserve, Category


# Flask error handlers
@app.errorhandler(NotFound)
def handle_not_found_error(error):
    return jsonify({'message': 'Resource not found'}), 404


@app.errorhandler(BadRequest)
def handle_bad_request_error(error):
    return jsonify({'message': 'Bad request'}), 400


@app.errorhandler(Unauthorized)
def handle_unauthorized_error(error):
    return jsonify({'message': 'Unauthorized'}), 401


@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    return jsonify({'message': 'Integrity error'}), 400


@app.errorhandler(NoResultFound)
def handle_no_result_found_error(error):
    return jsonify({'message': 'No result found'}), 404


# Flask routes
@app.route('/api/v1/users', methods=['POST'])
def create_new_user():
    data = request.get_json()
    try:
        user = create_user(uow, data)
        uow.commit()
        return jsonify({'id': user.ID}), 201
    except IntegrityError:
        uow.rollback()
        return jsonify({'message': 'User already exists'}), 409


@app.route('/api/v1/products', methods=['POST'])
def create_new_product():
    data = request.get_json()
    try:
        product = create_product(uow, data)
        uow.commit()
        return jsonify({'id': product.ID}), 201
    except IntegrityError:
        uow.rollback()
        return jsonify({'message': 'Product already exists'}), 409


@app.route('/api/v1/reserves', methods=['POST'])
def reserve_product_by_user():
    data = request.get_json()
    try:
        reserve = reserve_product(uow, data)
        uow.commit()
        return jsonify({'id': reserve.ID}), 201
    except IntegrityError:
        uow.rollback()
        return jsonify({'message': 'Reservation already exists'}), 409


@app.route('/api/v1/categories', methods=['POST'])
def create_new_category():
    data = request.get_json()
    try:
        category = create_category(uow, data)
        uow.commit()
        return jsonify({'id': category.ID}), 201
    except IntegrityError:
        uow.rollback()
        return jsonify({'message': 'Category already exists'}), 409


# Listen to domain events
@event.listens_for(ProductCreated, 'after_insert')
def product_created_listener(mapper, connection, target):
    uow.publish_events([target])


@event.listens_for(ProductUpdated, 'after_update')
def product_updated_listener(mapper, connection, target):
    uow.publish_events([target])


@event.listens_for(ProductDeleted, 'after_delete')
def product_deleted_listener(mapper, connection, target):
      uow.publish_events([target])
