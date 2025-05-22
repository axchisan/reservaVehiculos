async function registerUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('http://localhost:5001/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    const data = await response.json();
    alert(JSON.stringify(data));
}

async function fetchVehicles() {
    const response = await fetch('http://localhost:5002/vehicles');
    const vehicles = await response.json();
    const vehiclesDiv = document.getElementById('vehicles');
    vehiclesDiv.innerHTML = vehicles.map(v => `
        <div class="border p-4 rounded shadow">
            <h3 class="text-lg font-semibold">${v.brand} ${v.model}</h3>
            <p>Año: ${v.year}</p>
            <p>Precio por día: $${v.price_per_day}</p>
            <p>Disponible: ${v.available ? 'Sí' : 'No'}</p>
        </div>
    `).join('');
}

async function makeReservation() {
    const user_id = document.getElementById('user_id').value;
    const vehicle_id = document.getElementById('vehicle_id').value;
    const start_date = document.getElementById('start_date').value;
    const end_date = document.getElementById('end_date').value;
    
    const response = await fetch('http://localhost:5003/reservations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id, vehicle_id, start_date, end_date })
    });
    const data = await response.json();
    alert(JSON.stringify(data));
    fetchVehicles();
}

async function processPayment() {
    const reservation_id = document.getElementById('reservation_id').value;
    const amount = document.getElementById('amount').value;
    
    const response = await fetch('http://localhost:5004/payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reservation_id, amount })
    });
    const data = await response.json();
    alert(JSON.stringify(data));
}

document.addEventListener('DOMContentLoaded', fetchVehicles);