## Enfoques Pendientes de Trabajar

Debido al desbalanceo en las clases, debemos tomar enfoques mas complejos. Queremos tomar un enfoque híbrido como.

- **Aprendizaje Multiclase Jerárquico**
    - Un solo modelo que incorpore jerarquías (por ejemplo, BENIGN → Web Attack → Subtipo de Web Attack), podemos usar un modelo multicapa jerárquico:

    - Entrena un modelo con múltiples salidas, donde cada salida represente un nivel de la jerarquía.
    - Ejemplo:
        - Nivel 1: BENIGN vs MALICIOUS.
        - Nivel 2: Si es MALICIOUS, clasifica entre DDoS, PortScan, y WebAttack.
        - Nivel 3: Si es WebAttack, clasifica entre Brute Force, XSS, SQL Injection.
    - Esto puede implementarse usando redes neuronales con varias capas de salida o con varios modelos encadenados.

- **Técnicas de Ensemble**
    - Para mejorar la robustez de la clasificación, usa métodos de ensemble. Algunos ejemplos:

        - **Stacking**: Combina diferentes algoritmos (p. ej., Random Forest, Gradient Boosting, Neural Networks) y deja que un meta-modelo determine el resultado final.
        - **Bagging**: Entrena múltiples modelos con diferentes subconjuntos de datos (p. ej., Random Forest).
        - **Boosting**: Algoritmos como XGBoost, LightGBM o CatBoost son excelentes para manejar desbalance y detectar patrones complejos.
    - Se pueden usar estas técnicas tanto para el modelo principal como para los submodelos especializados.


- **Extra: Uso de Deep Learning**
    - Para problemas con características complejas y relaciones no lineales, como este, los modelos de deep learning pueden ser útiles:

        - **Autoencoders** para detección de anomalías: Utiliza autoencoders para detectar patrones maliciosos en general (sin especificar el tipo de ataque).
        - **Redes neuronales convolucionales (CNN)**: Si puedes transformar tus datos en imágenes (matrices de características), las CNN pueden ser efectivas.
        - **Redes recurrentes (RNN o LSTM)**: Si los datos tienen una componente temporal (tráfico de red en el tiempo), estas arquitecturas pueden capturar mejor la secuencia de eventos.