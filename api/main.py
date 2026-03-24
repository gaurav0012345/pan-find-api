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

    session = requests.Session()
    
    # 1. Pehle base page hit karte hain cookies ke liye
    try:
        session.get("https://www.bharatpan.com/retailer/findPan", timeout=10)
    except:
        pass

    url = "https://www.bharatpan.com/retailer/findPanProcessAPI"
    payload = {'aadhaar': aadhaar_no}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*",
        'X-Requested-With': "XMLHttpRequest",
        'Referer': "https://www.bharatpan.com/retailer/findpan",
        'Origin': "https://www.bharatpan.com",
        'Cookie': 'ci_session=2da8945321ce454cc1a0520b0b18bc2554ee4c8d' # <--- Aapki nikaali hui cookie
    }

    try:
        # 2. Request bhejte hain (allow_redirects=True rakhte hain check karne ke liye)
        response = session.post(url, data=payload, headers=headers, timeout=20)
        
        # Agar JSON milta hai toh thik, varna status code aur response text dikhayega
        try:
            return jsonify(response.json())
        except:
            # Agar blank aa raha hai toh yahan debug info dikhegi
            return jsonify({
                "status": "debug",
                "http_code": response.status_code,
                "server_response": response.text[:500], # Pehle 500 characters
                "url_accessed": response.url
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app = app
