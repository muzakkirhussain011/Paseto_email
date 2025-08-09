import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader, TensorDataset

URL = 'https://raw.githubusercontent.com/plotly/datasets/master/heart.csv'


def load_heart(test_size=0.2, batch_size=32, seed=0):
    df = pd.read_csv(URL)
    y = df['target'].values.astype(np.float32)
    s = df['sex'].values.astype(np.float32)
    X = df.drop(columns=['target']).values.astype(np.float32)
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X, y, s, test_size=test_size, random_state=seed)
    train_ds = TensorDataset(torch.tensor(X_train), torch.tensor(y_train), torch.tensor(s_train))
    test_ds = TensorDataset(torch.tensor(X_test), torch.tensor(y_test), torch.tensor(s_test))
    return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(test_ds, batch_size=batch_size)
