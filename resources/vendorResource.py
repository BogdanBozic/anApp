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
    if not response:#['vendors']:
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
    # import ipdb; ipdb.set_trace()
    payload = request.get_json()
    if not get_vendor_by_id(id):
        return jsonify({'error': 'Vendor with id {} does not exist.'.format(id)}), 404

    vendor = VendorModel.query_vendor_by_id(id)
    exists = False
    no_arguments = True
    try:
        vendor.name = payload['name']
        exists = True
        no_arguments = False
    except:
        pass
    try:
        vendor.address = payload['address']
        exists = True
        no_arguments = False
    except:
        pass
    try:
        vendor.phone_number = payload['phone_number']
        exists = True
        no_arguments = False
    except:
        pass
    try:
        vendor.email = payload['email']
        exists = True
        no_arguments = False
    except:
        pass
    try:
        vendor.notes = payload['notes']
        no_arguments = False
    except:
        pass

    if no_arguments:
        return jsonify({'error': 'No valid arguments provided.'}), 400
    # import ipdb; ipdb.set_trace()
    # if exists:
    #     if VendorModel.query_vendor_by_kwargs(**payload):
    #         return jsonify({'error': 'Invalid arguments or Vendor with this info already exists'}), 400
    submit = VendorModel.save_to_db(vendor)
    if type(submit) == tuple:
        return jsonify({'error': 'Vendor with {} already exists.'.format(submit[0])}), 400
    return VendorModel.query_vendor_by_id(id).json()



    """
    ЗАВРШАВАЈ ОВО, СИРОТИЉО
    """

