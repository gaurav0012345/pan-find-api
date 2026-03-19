from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Aapki API Key (Security ke liye)
MY_API_KEY = "ankit123"

@app.route('/get_pan', methods=['GET'])
def get_pan():
    # 1. API Key check karega
    user_key = request.args.get('key')
    if user_key != MY_API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 403

    # 2. Aadhaar Number lega
    aadhaar_no = request.args.get('aadhaar')
    if not aadhaar_no:
        return jsonify({"status": "error", "message": "Aadhaar number is required"}), 400

    # 3. BharatPan API se connect karega
    url = "https://www.bharatpan.com/retailer/findPanProcessAPI"
    
    payload = {
        'aadhaar': aadhaar_no
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'origin': "https://www.bharatpan.com",
        'referer': "https://www.bharatpan.com/retailer/findPan",
    }

    try:
        # BharatPan ko data bhej rahe hain
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        # BharatPan se jo bhi response aayega (JSON format mein), wo aapko dikhega
        return response.text 
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel ke liye ye line zaroori hai
app = app
