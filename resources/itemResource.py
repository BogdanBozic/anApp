from flask import jsonify, make_response, request
from model.itemModel import ItemModel
from flask import Blueprint
import ipdb

# from app import app

item_blueprint = Blueprint('item_blueprint', __name__)


@item_blueprint.route('/items', methods=['GET'])
def get_items():
    # if not request.args:
    return ItemModel.get_items().json()
    # else:
    #     ItemModel.name = request.args['name']
    #     ItemModel.vendor_id = request.args['vendor_id']
    #     ItemModel.price = request.args['price']
    #     items = ItemModel.get_item_by_multiple_parameters(ItemModel.name, ItemModel.vendor_id, ItemModel.price)
    #     return items


@item_blueprint.route('/items/<int:id>', methods=['GET'])
def get(id):
    # import ipdb; ipdb.set_trace()
    item = ItemModel.get_item_by_id(id)
    if item:
        return item.json()
    else:
        return jsonify({"message": "Item not found"}), 404


@item_blueprint.route('/items', methods=['POST'])
def post():
    # import ipdb; ipdb.set_trace()
    payload = request.get_json()
    try:
        payload['notes']
    except KeyError:
        payload['notes'] = ''

    try:
        new_item = ItemModel(name=payload['name'], price=payload['price'], vendor_id=payload['vendor_id'],
                             weight=payload['weight'], notes=payload['notes'])
    except KeyError as error:
        return jsonify({'error': "Missing required attribute {}".format(error)}), 400

    ItemModel.save_to_db(new_item)
    return ItemModel.get_item_by_name_and_vendor_id(name=new_item.name, vendor_id=new_item.vendor_id).json()
    # return jsonify(payload)


