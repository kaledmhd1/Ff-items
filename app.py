from flask import Flask, request, send_file, jsonify, redirect
import requests
from io import BytesIO

app = Flask(__name__)

ITEMS_JSON_URL = "https://items.kibomodz.online/items-json.json"

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "usage": "استخدم /item?id=رقم_العنصر لعرض صورة العنصر"
    })

@app.route('/item')
def get_item():
    item_id = request.args.get("id")

    if not item_id:
        return jsonify({"error": "يرجى إدخال رقم العنصر عبر ?id=123456"}), 400

    try:
        # جلب بيانات العناصر
        response = requests.get(ITEMS_JSON_URL)
        data = response.json()

        # البحث عن العنصر المطلوب
        for item in data:
            if str(item.get("item_id")) == str(item_id):
                image_url = item.get("image")
                # إعادة توجيه مباشر للصورة
                return redirect(image_url)

        return jsonify({"error": "العنصر غير موجود"}), 404

    except Exception as e:
        return jsonify({"error": f"حدث خطأ: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
