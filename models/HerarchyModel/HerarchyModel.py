import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import joblib
import xgboost as xgb


class HerarchyModel:
    def __init__(self):
        self.lvl1_model = None
        self.lvl2_model = None
        self.lvl3_model = None

    def load_models(self, lvl1_model, lvl2_model, lvl3_model, lvl1_columns=None, lvl2_columns=None, lvl3_columns=None):
        self.lvl1_model = joblib.load(lvl1_model)
        self.lvl2_model = tf.keras.models.load_model(lvl2_model)
        self.lvl3_model = joblib.load(lvl3_model)

        self.lvl1_columns = lvl1_columns
        self.lvl2_columns = lvl2_columns
        self.lvl3_columns = lvl3_columns

    def predict(self, X):
        # Verificar si los modelos están cargados
        if self.lvl1_model is None or self.lvl2_model is None or self.lvl3_model is None:
            raise Exception("Models not loaded")

        # Asegurarse de que X es un DataFrame
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        # Filtrar columnas para el modelo del nivel 1 si es necesario
        X_lvl1 = X[self.lvl1_columns] if self.lvl1_columns is not None else X
        y_pred_lvl1 = self.lvl1_model.predict(X_lvl1)

        # Inicializar una lista para las predicciones finales
        final_predictions = np.array([""] * len(X))

        # Asignar predicciones del nivel 1 que son "BENIGN"
        benign_mask = y_pred_lvl1 == "BENIGN"
        final_predictions[benign_mask] = "BENIGN"

        # Filtrar las filas que no son BENIGN para el nivel 2
        lvl2_indices = np.where(~benign_mask)[0]
        if len(lvl2_indices) > 0:
            X_lvl2 = X.iloc[lvl2_indices]
            if self.lvl2_columns is not None:
                X_lvl2 = X_lvl2[self.lvl2_columns]
            
            y_pred_lvl2 = self.lvl2_model.predict(X_lvl2)
            y_pred_lvl2 = np.argmax(y_pred_lvl2, axis=1)  # Convertir probabilidades a clases si aplica

            # Mapear las predicciones no-WebAttack directamente
            not_webattack_mask = y_pred_lvl2 != "WebAttack"
            final_predictions[lvl2_indices[not_webattack_mask]] = y_pred_lvl2[not_webattack_mask]

            # Filtrar filas que sí son WebAttack para el nivel 3
            lvl3_indices = lvl2_indices[~not_webattack_mask]
            if len(lvl3_indices) > 0:
                X_lvl3 = X.iloc[lvl3_indices]
                if self.lvl3_columns is not None:
                    X_lvl3 = X_lvl3[self.lvl3_columns]

                # Escalar las características para el modelo del nivel 3
                scaler = MinMaxScaler()
                X_lvl3_scaled = scaler.fit_transform(X_lvl3)

                y_pred_lvl3 = self.lvl3_model.predict(X_lvl3_scaled)
                final_predictions[lvl3_indices] = y_pred_lvl3

        return final_predictions
