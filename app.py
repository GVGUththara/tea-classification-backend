from flask import Flask, request, jsonify
from fiber_identification import identify_fiber_in_image
from stroke_identification import identify_stroke_in_image
from flask_cors import CORS

from PIL import Image
import io
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

# Function to convert an image array to Base64
def image_to_base64(image_array):
    image = Image.fromarray(image_array)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Endpoint: Identify Fiber
@app.route('/identify-fiber', methods=['POST'])
def identify_fiber():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read image and convert to OpenCV format
    image = Image.open(file).convert('RGB')
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Identify fiber
    result_image, stats = identify_fiber_in_image(image)

    print("Stats returned to frontend:", stats)

    # Convert result to base64
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    result_base64 = image_to_base64(result_image_rgb)

    return jsonify({
        "statistics": stats,
        "result_image": result_base64
    })


# Endpoint: Identify Stroke
@app.route('/identify-stroke', methods=['POST'])
def identify_stroke():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read image and convert to OpenCV format
    image = Image.open(file).convert('RGB')
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Identify stroke
    result_image, stats = identify_stroke_in_image(image)

    print("Stats returned to frontend:", stats)

    # Convert result to base64
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    result_base64 = image_to_base64(result_image_rgb)

    return jsonify({
        "statistics": stats,
        "result_image": result_base64
    })


if __name__ == '__main__':
    app.run(debug=True, port=8080)
