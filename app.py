<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>紅包計算機</title>
</head>
<body>
    <h1>紅包計算機</h1>
    
    <label for="city">選擇城市：</label>
    <select id="city" onchange="fetchHotels()">
        <option value="">請選擇</option>
        <option value="台北">台北</option>
        <option value="高雄">高雄</option>
    </select>
    
    <label for="hotel">選擇飯店：</label>
    <select id="hotel">
        <option value="">請先選擇城市</option>
    </select>
    
    <label for="people">人數：</label>
    <input type="number" id="people" value="1" min="1">
    
    <label for="extra">額外金額：</label>
    <input type="number" id="extra" value="0" min="0">
    
    <button onclick="calculateRedEnvelope()">計算紅包金額</button>
    
    <h2>計算結果：</h2>
    <p id="result"></p>
    
    <script>
        const API_BASE_URL = "https://red-envelope-api.onrender.com"; // 請更換為你的 Render API 網址
        
        async function fetchHotels() {
            const city = document.getElementById("city").value;
            const hotelSelect = document.getElementById("hotel");
            hotelSelect.innerHTML = '<option value="">請選擇飯店</option>';
            
            if (!city) return;
            
            const response = await fetch(`${API_BASE_URL}/hotels?city=${city}`);
            const hotels = await response.json();
            
            hotels.forEach(hotel => {
                let option = document.createElement("option");
                option.value = hotel.hotel;
                option.textContent = hotel.hotel;
                hotelSelect.appendChild(option);
            });
        }
        
        async function calculateRedEnvelope() {
            const hotel = document.getElementById("hotel").value;
            const people = document.getElementById("people").value;
            const extra = document.getElementById("extra").value;
            
            if (!hotel) {
                alert("請選擇飯店");
                return;
            }
            
            const response = await fetch(`${API_BASE_URL}/calculate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ hotel, people, extra })
            });
            
            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("result").textContent = `紅包金額: ${data.total} 元`;
            }
        }
    </script>
</body>
</html>
