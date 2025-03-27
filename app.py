from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

# 🔧 處理 Render 的 DATABASE_URL 格式（必須將 postgres:// 改為 postgresql://）
raw_db_url = os.environ.get("DATABASE_URL", "sqlite:///hotels.db")
if raw_db_url.startswith("postgres://"):
    raw_db_url = re.sub("^postgres://", "postgresql://", raw_db_url)

app.config["SQLALCHEMY_DATABASE_URI"] = raw_db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ✅ 部署時自動建立表格（若尚未存在）
with app.app_context():
    db.create_all()

@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
    return "資料表已建立！"


# 資料表定義
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

# API：根路徑測試用
@app.route('/')
def home():
    return "紅包計算 API 運行中！"

# API：查詢飯店
@app.route('/hotels', methods=['GET'])
def get_hotels():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "請提供城市名稱"}), 400
    hotels = Hotel.query.filter_by(city=city).all()
    return jsonify([{"city": h.city, "hotel": h.name, "price": h.price} for h in hotels])

# API：計算紅包金額
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    hotel_name = data.get("hotel")
    people = int(data.get("people", 1))
    extra = int(data.get("extra", 0))

    hotel = Hotel.query.filter_by(name=hotel_name).first()
    if not hotel:
        return jsonify({"error": "找不到指定飯店"}), 404

    total = hotel.price * people + extra
    return jsonify({"total": total})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
