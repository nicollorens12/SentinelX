class HierarchyModel:
    def __init__(self, model_lvl1, model_lvl2, model_lvl3, scaler, label_encoders):
        self.model_lvl1 = model_lvl1
        self.model_lvl2 = model_lvl2
        self.model_lvl3 = model_lvl3
        self.scaler = scaler
        self.label_encoders = label_encoders

    def train(self, X_train, y_train_lvl1, X_train_lvl2, y_train_lvl2, X_train_lvl3, y_train_lvl3):
        # Entrenar nivel 1
        self.model_lvl1.fit(X_train, y_train_lvl1)

        # Entrenar nivel 2
        self.model_lvl2.fit(X_train_lvl2, y_train_lvl2)

        # Entrenar nivel 3
        self.model_lvl3.fit(X_train_lvl3, y_train_lvl3)

    def predict(self, X):
        """
        Predicción jerárquica:
        Nivel 1: Predice entre BENIGN y MALIGN
        Nivel 2: Si la predicción es MALIGN, predice entre DDoS, PortScan y WebAttack
        Nivel 3: Si la predicción es WebAttack, predice entre BruteForce, XSS y SQLInjection
        """
        
        # Predicción del nivel 1: BENIGN vs MALIGN
        lvl1_pred = self.model_lvl1.predict(X)
        # Si el nivel 1 predice "MALIGN", pasa al nivel 2
        if lvl1_pred[0] == '1':
            print("FLAG")
            lvl2_pred = self.model_lvl2.predict(X)
            print("lvl2_pred: ", lvl2_pred)
            # Si el nivel 2 predice "WebAttack", pasa al nivel 3
            if lvl2_pred == 'WebAttack':
                lvl3_pred = self.model_lvl3.predict(X)
                print("lvl3_pred: ", lvl3_pred)
                if lvl3_pred == '0':
                    return "BruteForce"
                elif lvl3_pred == '1':
                    return "XSS"
                return "SQLInjection"
            else:
                return "PortScan" if lvl2_pred == '1' else "DDoS"
        else:
            return "BENIGN"  # Retornar la predicción del nivel 1 (BENIGN)