from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import process_model_and_predict, is_hdf5

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_content = file.read()

    if not is_hdf5(file_content):
        return jsonify({"error": "Invalid HDF5 file"}), 400

    try:
        result = process_model_and_predict(file_content)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
