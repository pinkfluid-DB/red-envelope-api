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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask API on port {port}")  # 這行會印出伺服器啟動狀態
    app.run(host='0.0.0.0', port=port)
