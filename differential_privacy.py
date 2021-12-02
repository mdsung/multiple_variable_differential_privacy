import numpy as np
from sklearn.preprocessing import MinMaxScaler

import config
from data import Original
from utils import read_csv_file, check_folder, mkdir_folder, write_pkl_file

from pathlib import Path
PROJECT_PATH = Path(__file__).parents[0]
METRIC_PATH = Path(PROJECT_PATH, 'metric')

class DiffPrivacy:
    def __init__(self, 
                original,
                output_folder: str):
             
        self.original = original
        self.original_data = original.data    
        self.levels = original.levels
        self.filter_category = original.filter_category

        self.output_folder = output_folder
    
    # @profile
    def get_diffrential_privacy_value(self, value: float, epsilon: float) -> float:
        """
        get differential privacy value
        to speed up, x divided into specific interval(10**4), and then using np.random.choice to get randomized value from pdf.
        """
        def pdf(x: float) -> float:
            """ bounded laplacian distribution pdf"""

            b = 2 / (epsilon)
            c = 1 - 0.5 * (np.exp(-(value + 1)/b) + np.exp(-(1 - value)/b))
            return 1 / (b * c * 2) * np.exp(-np.absolute(x - value)/b) 

        elements = np.linspace(-1, 1, 10**4)
        probabilities = pdf(elements)
        probabilities /= np.sum(probabilities)

        return np.random.choice(elements, size = 1, p = probabilities).item()

    def get_discretized_value(self, value: float, level:int) -> float: 
        """
        only categorical column value changed to discretirzed value
        level = 1, cardinality 1 -> value returns -1 
        level > 1, discretization
        """
        if level == 1:
            return -1

        ## pre calculate all values by arr Y
        beta = (value + 1) * (level - 1) / 2
        k = np.floor(beta)
        z1 = 2 * (k + 1) / (level - 1) - 1
        z2 = 2 * k / (level - 1) - 1
        p = (level - 1) * (value + 1) / 2 - k
        
        ## binom function to get {0, 1} by p 
        binom = lambda p_i:np.random.binomial(size = 1, n = 1, p = p_i)
        
        ## make Z vector by choosing z1, z2 using condition vector
        Z = np.where(binom(p), z1, z2)
        
        return Z

    def normalize(self, data: np.ndarray) -> np.ndarray:
        """
        min max normalization
        """
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        self.scaler.fit(data)
        return self.scaler.transform(data)

    def unnormalize(self, data:np.ndarray) -> np.ndarray:
        """
        un_normalized by inverse_transform
        """
        return self.scaler.inverse_transform(data)

    def save_data_to_pickle(self, data:np.ndarray, epsilon:float):
        """
        save numpy to pickle
        """
        ### create folder
        if not check_folder(self.output_folder):
            mkdir_folder(self.output_folder)
        
        ### save to pickle
        write_pkl_file(data, self.output_folder, f"{epsilon}.pkl")

    def dp(self, epsilon:float):
        # NORMALIZE
        data = self.normalize(self.original_data)

        # DP
        get_diffrential_privacy_value = np.vectorize(self.get_diffrential_privacy_value)
        data = get_diffrential_privacy_value(data, epsilon/data.shape[1])

        # DISC
        get_discretized_value = np.vectorize(self.get_discretized_value)
        data[:,self.filter_category] = get_discretized_value(data[:,self.filter_category], self.levels[self.filter_category])
        
        # UNNORMALIZE
        data = self.unnormalize(data)
        
        # SAVE
        self.save_data_to_pickle(data, epsilon)

def main():
    # configurations
    filename = config.DP_CONFIG["filename"]
    filedir = config.DP_CONFIG["filedir"]
    outputdir = config.DP_CONFIG["output_file_directory"]
    categorical_columns = config.DP_CONFIG["categorical_columns"] 
    epsilon_list = config.DP_CONFIG["epsilon_list"]
    
    import time
    from tqdm import tqdm
    import pandas as pd
    for count in tqdm([10, 100, 1000, 10000, 0]):
        epsilon_times = []
    
        original = Original(filedir, filename, categorical_columns, count) 
        diffprivacy = DiffPrivacy(
            original,
            outputdir,
        )
        
        for _ in tqdm(range(10)):
            epsilon_time = dict()
            for idx, epsilon in tqdm(enumerate(epsilon_list)):
                start = time.time()
                diffprivacy.dp(epsilon)
                elapse_time = time.time() - start
                epsilon_time[str(epsilon)] = elapse_time
                print(f"count={count}; epsilon={epsilon}; elapse_time={elapse_time};")
            epsilon_times.append(epsilon_time)
        
        pd.DataFrame.from_records(epsilon_times).to_feather(Path(METRIC_PATH, f"epsilon_times_count{count}.feather"))
        
if __name__ == "__main__":
    main()