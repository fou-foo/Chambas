import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def process_data(X,  categorical_features=[], num_features=[],   ohe=None, ordinal=None):

    X_categorical = X[categorical_features]
    X_continuous = X[num_features]

    X_categorical = ohe.transform(X_categorical)
    X_continuous = ordinal.transform(
        X_continuous[ordinal.get_feature_names_out()])

    X = np.concatenate([X_continuous, X_categorical], axis=1)
    return (X)
