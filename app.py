from flask import Flask, render_template, request, jsonify
from flask import send_from_directory

from scraper import get_video_url

app = Flask(__name__)

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"status": "error", "message": "URL kosong"})

    result = get_video_url(url)

    if not result:
        return jsonify({
            "status": "error",
            "message": "Video tidak ditemukan atau link tidak valid"
        })

    return jsonify({
        "status": "success",
        "sd": result.get("sd"),
        "hd": result.get("hd")
    })

if __name__ == "__main__":
    app.run(debug=True)
