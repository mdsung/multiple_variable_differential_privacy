# %%
from os import cpu_count
import pickle
from pathlib import Path

import pandas as pd
import ray

from data import Original
from differential_privacy import * 

try:
    PROJECT_PATH = Path(__file__).parents[0]
except NameError:
    PROJECT_PATH = Path('.').absolute()
DATA_PATH = Path(PROJECT_PATH, 'data')

# Read Original Data
data_A = pd.read_feather(Path(DATA_PATH, 'cc_data_A.feather'))
data_B = pd.read_feather(Path(DATA_PATH, 'cc_data_B.feather'))

# Split immutable and mutable data
data_A_immutable = data_A[['id', 'death', 'time']]
data_A_mutable = data_A.loc[:,'age':'antipsychotics']

with open(Path(PROJECT_PATH, "output_cc/A", "data_A_immutable.pkl"), 'wb') as f:
    pickle.dump(data_A_immutable, f)

with open(Path(PROJECT_PATH, "output_cc/A", "data_A_mutable.pkl"), 'wb') as f:
    pickle.dump(data_A_mutable, f)

data_B_immutable = data_B[['id', 'death', 'time']]
data_B_mutable = data_B[['stage4']]

with open(Path(PROJECT_PATH, "output_cc/B", "data_B_immutable.pkl"), 'wb') as f:
    pickle.dump(data_B_immutable, f)
    
with open(Path(PROJECT_PATH, "output_cc/B", "data_B_mutable.pkl"), 'wb') as f:
    pickle.dump(data_B_mutable, f)

# Create instance to run dp   
original_A = Original(data_A_mutable, ['sex', 'anxiolytic', 'antidepressant', 'antipsychotics']) 
original_B = Original(data_B_mutable, ['stage4']) 
diffprivacy_A = DiffPrivacy(original_A, "./output_cc/A")
diffprivacy_B = DiffPrivacy(original_B, "./output_cc/B")

# %%
ray.init(num_cpus = 32)

@ray.remote
def create_vetical_ldp_data(epsilon, attempt):
    diffprivacy_A.dp(epsilon)
    diffprivacy_B.dp(epsilon)  

    dp_data_A_mutable = pd.DataFrame(diffprivacy_A.final_data, columns = data_A_mutable.columns)
    dp_data_A = pd.concat([data_A_immutable, dp_data_A_mutable], axis = 1)

    dp_data_B_mutable = pd.DataFrame(diffprivacy_B.final_data, columns = data_B_mutable.columns)
    dp_data_B = pd.concat([data_B_immutable, dp_data_B_mutable], axis = 1)

    dp_data = pd.merge(dp_data_A, dp_data_B, on = ['id', 'death', 'time'])
    
    dp_data.to_feather(Path(f'output_cc/{epsilon}_{attempt}.feather'))
    
# %%
from itertools import product

attempt = 50
epsilon_list = [0.1, 1, 10, 100, 1000, 10000]
ray_instance = [create_vetical_ldp_data.remote(e, a) for e, a in product(epsilon_list, list(range(1, attempt + 1)))]
ray_result = ray.get(ray_instance)
