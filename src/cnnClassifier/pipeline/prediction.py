import numpy as np
from tensorflow import keras
from keras.models import load_model
from keras.api.keras.preprocessing import image
from postgres_database.config import read_config
from postgres_database.database import connect_to_database, execute_query, close_connection
# from tensorflow.python.keras.models import load_model
# from tensorflow.python.keras.appreprocessing import image
import os
import psycopg2
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
logger = logging.getLogger("cnnClassifierLogger")
logger.addHandler(logging.FileHandler("running_logs.log"))
logger.addHandler(logging.StreamHandler())


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # Load model
        model = load_model(os.path.join("artifacts", "training", "model.h5"))

        # Load and preprocess image
        imagename = self.filename
        test_image = image.load_img(imagename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Make prediction
        result = model.predict(test_image)[0]
        print(result)
        prediction_label = 'Normal' if np.argmax(result) == 1 else 'Adenocarcinoma Cancer'

        # Store prediction result in PostgreSQL
        self.store_result(result, prediction_label)

        return [{"image": prediction_label}]

    def store_result(self, result, prediction_label):
        db_params = read_config()

        try:
            with psycopg2.connect(**db_params) as conn, conn.cursor() as cursor:
                print("connection is successful")
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS public.result_table (
                        id SERIAL PRIMARY KEY,
                        loss NUMERIC,
                        accuracy NUMERIC,
                        image VARCHAR(255),
                        predicted_result VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );"""
                cursor.execute(create_table_query)

                insert_query = """
                    INSERT INTO public.result_table (loss, accuracy, image, predicted_result)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (float(result[0]), float(result[1]), 'image', prediction_label)
                )
                conn.commit()

        except Exception as e:
            print(f"Error: {e}")

