import io
import h5py
import numpy as np
import base64
from PIL import Image
from matplotlib.colors import ListedColormap
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import AUC
from keras.saving import register_keras_serializable
import matplotlib.pyplot as plt

# ---------------- Register custom metrics ---------------- #

@register_keras_serializable()
def f1_m(y_true, y_pred):
    y_pred_binary = np.round(y_pred)
    tp = np.sum(np.round(y_true * y_pred_binary))
    precision = tp / (np.sum(np.round(y_pred_binary)) + 1e-7)
    recall = tp / (np.sum(np.round(y_true)) + 1e-7)
    return 2 * ((precision * recall) / (precision + recall + 1e-7))

@register_keras_serializable()
def precision_m(y_true, y_pred):
    y_pred_binary = np.round(y_pred)
    tp = np.sum(np.round(y_true * y_pred_binary))
    predicted_positives = np.sum(np.round(y_pred_binary))
    return tp / (predicted_positives + 1e-7)

@register_keras_serializable()
def recall_m(y_true, y_pred):
    y_pred_binary = np.round(y_pred)
    tp = np.sum(np.round(y_true * y_pred_binary))
    possible_positives = np.sum(np.round(y_true))
    return tp / (possible_positives + 1e-7)

# ---------------- Load model ---------------- #

model = load_model('backend/best_model.keras', custom_objects={
    "f1_m": f1_m,
    "precision_m": precision_m,
    "recall_m": recall_m,
    "AUC": AUC()
})

# ---------------- HDF5 Check ---------------- #

def is_hdf5(file_bytes):
    return file_bytes[:8] == b'\x89HDF\r\n\x1a\n'

# ---------------- Prediction + Visualization ---------------- #

def process_model_and_predict(file_bytes):
    with h5py.File(io.BytesIO(file_bytes), 'r') as h5file:
        data = h5file['img'][:]

    # Preprocessing
    data[np.isnan(data)] = 0.000001
    mid_rgb = data[:, :, 1:4].max() / 2.0
    mid_slope = data[:, :, 12].max() / 2.0
    mid_elevation = data[:, :, 13].max() / 2.0

    red = data[:, :, 3]
    green = data[:, :, 2]
    blue = data[:, :, 1]
    nir = data[:, :, 7]
    ndvi = np.divide(nir - red, nir + red + 1e-7)

    img_data = np.zeros((1, 128, 128, 6))
    img_data[0, :, :, 0] = 1 - red / mid_rgb
    img_data[0, :, :, 1] = 1 - green / mid_rgb
    img_data[0, :, :, 2] = 1 - blue / mid_rgb
    img_data[0, :, :, 3] = ndvi
    img_data[0, :, :, 4] = 1 - data[:, :, 12] / mid_slope
    img_data[0, :, :, 5] = 1 - data[:, :, 13] / mid_elevation

    # Prediction
    pred = model.predict(img_data)
    mask = (pred[0, :, :, 0] > 0.5).astype(np.uint8)
    label = "Yes" if pred[0, :, :, 0].mean() > 0.5 else "No"

    # Original RGB image
    rgb = np.stack([
        (red / red.max() * 255).astype(np.uint8),
        (green / green.max() * 255).astype(np.uint8),
        (blue / blue.max() * 255).astype(np.uint8),
    ], axis=-1)
    original_pil = Image.fromarray(rgb)

    # Predicted mask image (green for safe, red for landslide)
    pred_overlay = np.zeros((128, 128, 3), dtype=np.uint8)
    pred_overlay[mask == 0] = [0, 255, 0]   # Green
    pred_overlay[mask == 1] = [255, 0, 0]   # Red
    pred_pil = Image.fromarray(pred_overlay)

    # Convert both to base64
    def to_base64(pil_image):
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    original_base64 = to_base64(original_pil)
    predicted_base64 = to_base64(pred_pil)

    return {
        "original": original_base64,
        "predicted": predicted_base64,
        "prediction": label
    }
