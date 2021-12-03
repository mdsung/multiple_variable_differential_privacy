import os
from typing import List

import numpy as np
import pandas as pd

from utils import read_csv_file, read_feather_file, read_pkl_file, get_categorical_levels_from_data

class Original:
    def __init__(self, 
                 data:pd.DataFrame, 
                 categorical_columns:List):

        # full_file_name = os.path.join(filedir, filename)
        # if "csv" in full_file_name:
        #     read_file = read_csv_file
        # elif 'feather' in full_file_name:
        #     read_file = read_feather_file
            
        # if count == 0:
        #     self.data = read_file(full_file_name)
        # elif count > 0:
        #     self.data = read_file(full_file_name).iloc[:count]
        self.data = data 
        self.categorical_columns = categorical_columns
        self.continuous_columns = [d for d in self.data if d not in categorical_columns]

        self.levels = self._get_levels()
        self.filter_category = self.levels > 0
        self.filter_continuous = self.levels == 0

        self.data = self.data.to_numpy()

    def _get_levels(self) -> np.ndarray:
        return np.array([get_categorical_levels_from_data(self.data, d) if d in self.categorical_columns else 0 for d in self.data])

class Label:
    def __init__(self, filedir:str, filename:str, original):
        full_file_name = os.path.join(filedir, filename)
        self.data = read_csv_file(full_file_name).to_numpy().ravel()
        self.row_number = original.data.shape[0]
        self._validate_label_data()
    
    def _validate_label_data(self):
        assert self.data.shape[0] == self.row_number, "label shape will be same with data shape."
            
class Data:
    def __init__(self, epsilon:int, outputdir:str):
        self.epsilon = epsilon
        self.outputdir = outputdir
        self._get_data()

    def _get_data(self):
        self.data = read_pkl_file(os.path.join(self.outputdir, f"{self.epsilon}.pkl"))