from flask import request, jsonify, make_response
from model.vendorModel import VendorModel
from flask import Blueprint

vendor_blueprint = Blueprint('vendor_blueprint', __name__)


@vendor_blueprint.route('/vendors/<int:id>', methods=['GET'])
def get_vendor_by_id(id):
    vendor = VendorModel.query_vendor_by_id(id)
    if vendor:
        return vendor.json()
    else:
        return jsonify({'message': 'Vendor with id {} not found'.format(id)})


@vendor_blueprint.route('/vendors', methods=['GET'])
def get_vendor_by_kwargs():
    if not request.args:
        return VendorModel.query_vendors()
    dictionary = request.args.to_dict()
    response = VendorModel.query_vendor_by_kwargs(**dictionary)
    if type(response) == str:
        return jsonify({'error': 'attribute with name {} does not exist'.format(response)}), 400
    if not response['vendors']:
        return jsonify({'error': 'Vendor not found.'}), 404
    return response


@vendor_blueprint.route('/vendors', methods=['POST'])
def post():
    payload = request.get_json()
    try:
        payload['notes']
    except KeyError:
        payload['notes'] = ''

    vendor_doesnt_exist, vendor_exists_error_message = VendorModel.check_if_vendor_exists(name=payload['name'],
                                                                                          phone_number=payload[
                                                                                              'phone_number'],
                                                                                          email=payload['email'],
                                                                                          address=payload['address'])

    if vendor_doesnt_exist:
        new_vendor = VendorModel(name=payload['name'], phone_number=payload['phone_number'], email=payload['email'],
                                 address=payload['address'], notes=payload['notes'])

        VendorModel.save_to_db(new_vendor)
        return VendorModel.query_vendor_by_kwargs(**{'email': payload['email']})
    else:
        return jsonify({'error': "Vendor with this {} already exists.".format(vendor_exists_error_message)}), 400


@vendor_blueprint.route('/vendors/<int:id>', methods=['PUT'])
def edit_vendor(id):
    payload = request.get_json()
    if not get_vendor_by_id(id):
        return jsonify({'error': 'Vendor with id {} does not exist.'.format(id)}), 404
    updated_vendor = VendorModel
    try:
        updated_vendor.name = payload['name']
    except:
        pass
    try:
        updated_vendor.address = payload['address']
    except:
        pass
    try:
       updated_vendor.phone_number = payload['phone_number']
    except:
        pass
    try:
        updated_vendor.email = payload['email']
    except:
        pass
    try:
        updated_vendor.notes = payload['notes']
    except:
        pass
    VendorModel.save_to_db(updated_vendor)
    return VendorModel.query_vendor_by_kwargs(**updated_vendor)



    """
    ЗАВРШАВАЈ ОВО, СИРОТИЉО
    """

