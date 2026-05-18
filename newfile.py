from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/video")
def video():

    url = request.args.get("url", "").strip()

    if not url:
        return jsonify({
            "status": "error",
            "msg": "empty url"
        })

    try:

        ydl_opts = {
            "quiet": True,
            "format": "best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            direct_url = info["url"]

            return jsonify({
                "status": "ok",
                "download": direct_url,
                "title": info.get("title", "video")
            })

    except Exception as e:

        return jsonify({
            "status": "error",
            "msg": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)