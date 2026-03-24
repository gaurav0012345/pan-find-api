from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MY_API_KEY = "ankit123"

@app.route('/get_pan', methods=['GET'])
def get_pan():
    user_key = request.args.get('key')
    if user_key != MY_API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 403

    aadhaar_no = request.args.get('aadhaar')
    if not aadhaar_no:
        return jsonify({"status": "error", "message": "Aadhaar number missing"}), 400

    # Ek session create karein taaki cookies handle ho sakein
    session = requests.Session()
    
    # Pehle main page par ek "GET" request bhejein taaki CSRF ya Cookies mil jayein
    session.get("https://www.bharatpan.com/retailer/findPan", timeout=10)

    url = "https://www.bharatpan.com/retailer/findPanProcessAPI"
    
    payload = {'aadhaar': aadhaar_no}

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-Requested-With': "XMLHttpRequest",
        'Referer': "https://www.bharatpan.com/retailer/findPan",
        'Origin': "https://www.bharatpan.com"
    }

    try:
        # allow_redirects=False lagaya hai taaki home page par redirect na ho
        response = session.post(url, data=payload, headers=headers, timeout=15, allow_redirects=False)
        
        if response.status_code == 302:
            return jsonify({"status": "error", "message": "Server Redirected to Home (Blocked by BharatPan)"}), 401

        try:
            return jsonify(response.json())
        except:
            return response.text

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app = app
