from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "紅包計算 API 運行中！"

@app.route('/hotels', methods=['GET'])
def get_hotels():
    city = request.args.get('city')
    hotels = [
        {"city": "台北", "hotel": "台北大倉久和大飯店", "price": 4100},
        {"city": "高雄", "hotel": "高雄漢來大飯店", "price": 3800}
    ]
    return jsonify([h for h in hotels if h["city"] == city])

@app.route('/calculate', methods=['POST'])
def calculate_red_envelope():
    data = request.json
    hotel_name = data.get("hotel")
    people = int(data.get("people", 1))
    extra = int(data.get("extra", 0))
    
    hotels = [
        {"city": "台北", "hotel": "台北大倉久和大飯店", "price": 4100},
        {"city": "高雄", "hotel": "高雄漢來大飯店", "price": 3800}
    ]
    
    hotel = next((h for h in hotels if h["hotel"] == hotel_name), None)
    if not hotel:
        return jsonify({"error": "找不到指定飯店"}), 404

    total_amount = hotel["price"] * people + extra
    return jsonify({"total": total_amount})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
