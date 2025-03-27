from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 設定 SQLAlchemy 連接 Render 資料庫
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///hotels.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 定義資料庫表（飯店資訊）
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

# 查詢飯店 API
@app.route('/hotels', methods=['GET'])
def get_hotels():
    city = request.args.get('city')
    hotels = Hotel.query.filter_by(city=city).all()
    return jsonify([{"city": h.city, "hotel": h.name, "price": h.price} for h in hotels])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/calculate', methods=['POST'])
def calculate_red_envelope():
    data = request.json
    hotel_name = data.get("hotel")
    people = int(data.get("people", 1))
    extra = int(data.get("extra", 0))

    # 從資料庫查詢該飯店
    hotel = Hotel.query.filter_by(name=hotel_name).first()
    if not hotel:
        return jsonify({"error": "找不到指定飯店"}), 404

    total = hotel.price * people + extra
    return jsonify({"total": total})

