from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

COOKIE_FILE = "cookies.txt"


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "msg": "yt-dlp API running 🚀"
    })


@app.route("/video")
def video():
    url = request.args.get("url", "").strip()

    if not url:
        return jsonify({
            "status": "error",
            "msg": "empty url"
        }), 400

    try:
        ydl_opts = {
    "quiet": True,
    "noplaylist": True,
    "format": "bv*[ext=mp4]+ba/best",
    "merge_output_format": "mp4",
    "cookiefile": COOKIE_FILE
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return jsonify({
                "status": "ok",
                "title": info.get("title"),
                "download": info.get("url"),
                "duration": info.get("duration")
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "msg": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
