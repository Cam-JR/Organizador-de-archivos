from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, sys
from organizer import organize_by_type, organize_by_date

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/organize", methods=["POST"])
def organize():
    data = request.get_json()
    folder = data.get("folder")
    mode = data.get("mode", "type")  # "type" o "date"
    date_by = data.get("dateBy", "modified")  # "modified" o "created"

    if not folder or not os.path.exists(folder):
        return jsonify({"error": "Carpeta no encontrada"}), 400

    try:
        if mode == "type":
            result = organize_by_type(folder)
        elif mode == "date":
            result = organize_by_date(folder, by=date_by)
        else:
            return jsonify({"error": "Modo no válido"}), 400

        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 👇 ESTA PARTE VA ANTES DEL app.run()
@app.route("/preview", methods=["POST"])
def preview():
    data = request.get_json()
    folder = data.get("folder")
    mode = data.get("mode", "type")
    date_by = data.get("dateBy", "modified")

    if not folder or not os.path.exists(folder):
        return jsonify({"error": "Carpeta no encontrada"}), 400

    try:
        if mode == "type":
            from organizer import simulate_by_type
            result = simulate_by_type(folder)
        elif mode == "date":
            from organizer import simulate_by_date
            result = simulate_by_date(folder, by=date_by)
        else:
            return jsonify({"error": "Modo no válido"}), 400

        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 👇 El bloque principal siempre va al final
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
