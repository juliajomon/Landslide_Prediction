import os
import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.models import load_model


# Ensure the uploads folder exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to process the H5 file
def process_h5(file_path):
    try:
        # Load H5 file
        with h5py.File(file_path, "r") as hf:
            # Assuming the dataset is named 'data', modify if needed
            if "data" in hf:
                data = np.array(hf["data"])
            else:
                raise KeyError("Dataset 'data' not found in .h5 file")

        # Generate and save the image
        img_path = os.path.join(UPLOAD_FOLDER, os.path.basename(file_path).replace(".h5", ".png"))
        plt.imshow(data, cmap="gray")
        plt.axis("off")
        plt.savefig(img_path, bbox_inches="tight")
        plt.close()
        print(f"Image saved at: {img_path}")

        return img_path

    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# Function to predict landslide (dummy model for now)
def predict_landslide(image_path, model_path="model/model.h5"):
    try:
        # Load the model
        model = load_model(model_path)

        # Load the image as input data
        img = plt.imread(image_path)
        img_resized = np.expand_dims(img, axis=0)  # Reshape for model

        # Get prediction
        prediction = model.predict(img_resized)
        result = "Yes" if prediction[0][0] > 0.5 else "No"
        print(f"Landslide Prediction: {result}")

        return result
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

# If running as script, process file from argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_h5_file>")
        sys.exit(1)

    h5_file = sys.argv[1]
    img_path = process_h5(h5_file)
    if img_path:
        predict_landslide(img_path)
