from sklearn.datasets import fetch_openml
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset


def load_adult(test_size=0.2, batch_size=64, seed=0):
    data = fetch_openml('adult', version=2, as_frame=True, parser='auto')
    df = data.frame
    y = (df['class'] == '>50K').astype(np.float32).values
    s = (df['sex'] == 'Male').astype(np.float32).values
    X = df.drop(columns=['class']).astype(str)
    enc = OneHotEncoder(handle_unknown='ignore')
    X_enc = enc.fit_transform(X).astype(np.float32)
    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X_enc, y, s, test_size=test_size, random_state=seed)
    X_train = torch.tensor(X_train.toarray())
    X_test = torch.tensor(X_test.toarray())
    train_ds = TensorDataset(X_train, torch.tensor(y_train), torch.tensor(s_train))
    test_ds = TensorDataset(X_test, torch.tensor(y_test), torch.tensor(s_test))
    return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(test_ds, batch_size=batch_size)
