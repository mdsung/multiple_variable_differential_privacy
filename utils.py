import os
import pickle
import pandas as pd
import numpy as np

def read_csv_file(filename):
    return pd.read_csv(filename)

def read_feather_file(filename):
    return pd.read_feather(filename)

def read_pkl_file(fullfilepath):
    with open(fullfilepath, "rb") as f:
        return pickle.load(f)

def write_pkl_file(data, filepath, filename):
    with open(os.path.join(filepath, filename), "wb") as f:
        pickle.dump(data, f)

def check_folder(folder):
    return os.path.isdir(folder)

def mkdir_folder(folder):
    os.mkdir(folder)
    
def get_categorical_levels_from_data(data:np.ndarray, col: str) -> int:
    sr = data.loc[:, col].astype(int)
    return int(sr.max() - sr.min() + 1)