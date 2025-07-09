from flask import Blueprint, jsonify, request
from models import Shop
from services.location_service import location_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/shops')
def api_shops():
    shops = Shop.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': shop.id,
        'name': shop.name,
        'latitude': shop.latitude,
        'longitude': shop.longitude,
        'address': shop.address,
        'rating': shop.average_rating,
        'is_open': shop.is_open
    } for shop in shops])

@api_bp.route('/api/geocode')
def api_geocode():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address parameter required'}), 400
    
    try:
        coordinates = location_service.geocode_address(address)
        if coordinates:
            return jsonify({
                'latitude': coordinates[0],
                'longitude': coordinates[1]
            })
        else:
            return jsonify({'error': 'Address not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/reverse-geocode')
def api_reverse_geocode():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude parameters required'}), 400
    
    try:
        address = location_service.reverse_geocode(float(lat), float(lng))
        if address:
            return jsonify({'address': address})
        else:
            return jsonify({'error': 'Address not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/health-check', methods=['HEAD', 'GET'])
def health_check():
    return '', 200