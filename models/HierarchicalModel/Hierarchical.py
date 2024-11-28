import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
import joblib

class HierarchyModel(BaseEstimator, ClassifierMixin):
    def __init__(self, model_lvl1, model_lvl2, model_lvl3, encoder_lvl2=None, encoder_lvl3=None):
        """
        Clase para gestionar predicciones jerárquicas con múltiples modelos.

        :param model_lvl1: Modelo entrenado para el nivel 1 (BENIGN/MALIGN).
        :param model_lvl2: Modelo entrenado para el nivel 2 (WebAttack u otras clases malignas).
        :param model_lvl3: Modelo entrenado para el nivel 3 (ataques específicos como XSS, SQLInjection, etc.).
        :param encoder_lvl2: Codificador de etiquetas para el nivel 2 (opcional).
        :param encoder_lvl3: Codificador de etiquetas para el nivel 3 (opcional).
        """
        self.model_lvl1 = joblib.load(model_lvl1)
        self.model_lvl2 = joblib.load(model_lvl2)
        self.model_lvl3 = joblib.load(model_lvl3)
        self.encoder_lvl2 = joblib.load(encoder_lvl2) if encoder_lvl2 else None
        self.encoder_lvl3 = joblib.load(encoder_lvl3) if encoder_lvl3 else None

    def predict(self, X):
        """
        Realiza predicciones jerárquicas utilizando los modelos entrenados.

        :param X: Datos de entrada.
        :return: Predicciones finales combinadas.
        """
        # Predicción de nivel 1
        y_pred_lvl1 = self.model_lvl1.predict(X)

        # Máscara para nivel 2 (MALIGN casos)
        lvl2_mask = y_pred_lvl1 == 'MALIGN'
        X_lvl2 = X[lvl2_mask]

        if X_lvl2.shape[0] > 0:
            # Predicción de nivel 2
            y_pred_lvl2 = self.model_lvl2.predict(X_lvl2)
            if self.encoder_lvl2:
                y_pred_lvl2 = self.encoder_lvl2.inverse_transform(y_pred_lvl2)

            # Actualizar predicciones en los datos malignos
            y_pred_lvl1[lvl2_mask] = y_pred_lvl2

            # Máscara para nivel 3 (WebAttack casos)
            lvl3_mask = y_pred_lvl1 == 'WebAttack'
            X_lvl3 = X[lvl3_mask]

            if X_lvl3.shape[0] > 0:
                # Predicción de nivel 3
                y_pred_lvl3 = self.model_lvl3.predict(X_lvl3)
                if self.encoder_lvl3:
                    y_pred_lvl3 = self.encoder_lvl3.inverse_transform(y_pred_lvl3)

                # Actualizar predicciones en los datos de ataques web
                y_pred_lvl1[lvl3_mask] = y_pred_lvl3

        return y_pred_lvl1
