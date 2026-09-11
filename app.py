from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_prescription():

    if "prescription" not in request.files:
        return jsonify({"error": "Please upload a prescription image"})

    file = request.files["prescription"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)

        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            extracted_text = "Unable to read prescription clearly."

        translated_text = str(extracted_text)

        return jsonify({
            "extracted_text": extracted_text,
            "translated_text": translated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)