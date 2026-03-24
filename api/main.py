from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Aapki API Key (Security ke liye)
MY_API_KEY = "ankit123"

@app.route('/')
def home():
    return "API is Live! Use /get_pan?key=ankit123&aadhaar=YOUR_AADHAAR"

@app.route('/get_pan', methods=['GET'])
def get_pan():
    # 1. API Key check karega
    user_key = request.args.get('key')
    if user_key != MY_API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 403

    # 2. Aadhaar Number lega
    aadhaar_no = request.args.get('aadhaar')
    if not aadhaar_no:
        return jsonify({"status": "error", "message": "Aadhaar number missing"}), 400

    # 3. BharatPan API Settings
    url = "https://www.bharatpan.com/retailer/findPanProcessAPI"
    
    payload = {
        'aadhaar': aadhaar_no
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Language': "en-US,en;q=0.9,hi;q=0.8",
        'Referer': "https://www.bharatpan.com/retailer/findPan",
        'X-Requested-With': "XMLHttpRequest",
        'Origin': "https://www.bharatpan.com",
        'Connection': "keep-alive"
    }

    try:
        # BharatPan ko request bhej rahe hain
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        
        # Agar response JSON hai toh JSON bhejein, varna text
        try:
            return jsonify(response.json())
        except:
            return response.text

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel deployment ke liye ye line sabse zaroori hai
app = app
