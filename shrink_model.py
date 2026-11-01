"""Re-save the trained model without optimizer state so it fits in Streamlit Cloud memory."""
import os

import gdown
import tensorflow as tf

FULL_MODEL_ID = "1j9da4mKD7t3TjWXAEN5-Cxq1vtHgI7lc"
FULL_MODEL_PATH = "age_gender_prediction_model_full.keras"
SLIM_MODEL_PATH = "age_gender_prediction_model.keras"

if not os.path.exists(FULL_MODEL_PATH):
    gdown.download(id=FULL_MODEL_ID, output=FULL_MODEL_PATH, quiet=False)

model = tf.keras.models.load_model(FULL_MODEL_PATH, compile=False)
model.save(SLIM_MODEL_PATH)

print(f"Saved {SLIM_MODEL_PATH}: {os.path.getsize(SLIM_MODEL_PATH) / 1e6:.0f} MB")
