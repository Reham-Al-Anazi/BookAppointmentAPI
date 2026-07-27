from flask import Flask, request, jsonify

app = Flask(__name__)

appointments = [
    {"id": 1, "city": "Riyadh", "date": "2025-05-03", "time": "04:23"}
]

# 1. جلب المواعيد
@app.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify(appointments), 200

# 2. إضافة موعد جديد
@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    new_app = {
        "id": len(appointments) + 1,
        "city": data.get('city'),
        "date": data.get('date'),
        "time": data.get('time')
    }
    appointments.append(new_app)
    return jsonify(new_app), 201

# 3. تعديل موعد
@app.route('/appointments/<int:app_id>', methods=['PUT'])
def update_appointment(app_id):
    data = request.get_json()
    for appt in appointments:
        if appt["id"] == app_id:
            appt.update({
                "city": data.get('city', appt["city"]),
                "date": data.get('date', appt["date"]),
                "time": data.get('time', appt["time"])
            })
            return jsonify(appt), 200
    return jsonify({"error": "Not found"}), 404

# 4. حذف موعد
@app.route('/appointments/<int:app_id>', methods=['DELETE'])
def delete_appointment(app_id):
    global appointments
    initial_len = len(appointments)
    appointments = [appt for appt in appointments if appt["id"] != app_id]
    
    if len(appointments) < initial_len:
        return jsonify({"message": "Deleted successfully"}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)