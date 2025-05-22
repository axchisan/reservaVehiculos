from flask import Blueprint, request, jsonify # type: ignore
from app.models import Reservation, db
from datetime import datetime
import requests # type: ignore

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('vehicle_id') or not data.get('start_date') or not data.get('end_date'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verificar usuario
    user_response = requests.get(f'http://user_service:5001/users/{data["user_id"]}')
    if user_response.status_code != 200:
        return jsonify({'error': 'Invalid user'}), 400
    
    # Verificar vehículo
    vehicle_response = requests.get(f'http://vehicle_service:5002/vehicles/{data["vehicle_id"]}')
    if vehicle_response.status_code != 200 or not vehicle_response.json()['available']:
        return jsonify({'error': 'Vehicle not available'}), 400
    
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    days = (end_date - start_date).days
    if days <= 0:
        return jsonify({'error': 'Invalid date range'}), 400
    
    total_price = days * vehicle_response.json()['price_per_day']
    new_reservation = Reservation(user_id=data['user_id'], vehicle_id=data['vehicle_id'], start_date=start_date, end_date=end_date, total_price=total_price)
    db.session.add(new_reservation)
    db.session.commit()
    
    # Marcar vehículo como no disponible
    requests.put(f'http://vehicle_service:5002/vehicles/{data["vehicle_id"]}', json={'available': False})
    
    return jsonify({'id': new_reservation.id, 'user_id': new_reservation.user_id, 'vehicle_id': new_reservation.vehicle_id, 'start_date': str(new_reservation.start_date), 'end_date': str(new_reservation.end_date), 'total_price': new_reservation.total_price, 'status': new_reservation.status}), 201