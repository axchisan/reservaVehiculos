from flask import Blueprint, request, jsonify
from app.models import Payment, db
import requests

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data or not data.get('reservation_id') or not data.get('amount'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verificar reserva
    reservation_response = requests.get(f'http://reservation_service:5003/reservations/{data["reservation_id"]}')
    if reservation_response.status_code != 200:
        return jsonify({'error': 'Invalid reservation'}), 400
    
    new_payment = Payment(reservation_id=data['reservation_id'], amount=data['amount'])
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({'id': new_payment.id, 'reservation_id': new_payment.reservation_id, 'amount': new_payment.amount, 'payment_date': str(new_payment.payment_date), 'status': new_payment.status}), 201