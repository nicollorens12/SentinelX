import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib


class HerarchyModel:
    def __init__(self):
        self.lvl1_model = None
        self.lvl2_model = None
        self.lvl3_model = None
        
    def load_models(self, lvl1_model, lvl2_model, lvl3_model):
        rf = joblib.load(lvl1_model)
        self.lvl1_model = rf
        
        nn = tf.keras.models.load_model(lvl2_model)
        self.lvl2_model = nn
        
        xgboost = joblib.load(lvl3_model)
        self.lvl3_model = xgboost
        
    def predict(self, X):
        

