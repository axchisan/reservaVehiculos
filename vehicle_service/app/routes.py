from flask import Blueprint, request, jsonify
from app.models import Vehicle, db

vehicle_bp = Blueprint('vehicle', __name__)

@vehicle_bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not data or not data.get('model') or not data.get('brand') or not data.get('year') or not data.get('price_per_day'):
        return jsonify({'error': 'Missing required fields'}), 400
    new_vehicle = Vehicle(model=data['model'], brand=data['brand'], year=data['year'], price_per_day=data['price_per_day'])
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'id': new_vehicle.id, 'model': new_vehicle.model, 'brand': new_vehicle.brand, 'year': new_vehicle.year, 'price_per_day': new_vehicle.price_per_day, 'available': new_vehicle.available}), 201

@vehicle_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.filter_by(available=True).all()
    return jsonify([{'id': v.id, 'model': v.model, 'brand': v.brand, 'year': v.year, 'price_per_day': v.price_per_day, 'available': v.available} for v in vehicles])