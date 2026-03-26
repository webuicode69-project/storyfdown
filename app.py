from flask import Flask, render_template, request, jsonify
from flask import send_from_directory

from scraper import get_video_url

app = Flask(__name__)

@app.route("/robots.txt")
def robots():
    return """User-agent: *
Allow: /

Sitemap: https://bot-lwq9.onrender.com/sitemap.xml
""", 200, {'Content-Type': 'text/plain'}
    
@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://bot-lwq9.onrender.com/</loc>
    <priority>1.0</priority>
  </url>
</urlset>
""", 200, {'Content-Type': 'application/xml'}

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
