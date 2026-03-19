from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Aapki API Key (ise aap badal bhi sakte hain)
MY_API_KEY = "ankit123"

@app.route('/get_pan', methods=['GET'])
def get_pan():
    # API Key check karega
    user_key = request.args.get('key')
    if user_key != MY_API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 403

    aadhaar_no = request.args.get('aadhaar')
    if not aadhaar_no:
        return jsonify({"status": "error", "message": "Aadhaar number missing"}), 400

    url = "https://www.bharatpan.com/retailer/findPanProcessAPI"
    payload = {'aadhaar': aadhaar_no}
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'origin': "https://www.bharatpan.com",
        'referer': "https://www.bharatpan.com/retailer/findPan",
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.text
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500