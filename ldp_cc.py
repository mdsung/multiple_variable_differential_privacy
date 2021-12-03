# %%
import pickle
import pandas as pd
from data import Original
from differential_privacy import * 
from pathlib import Path
try:
    PROJECT_PATH = Path(__file__).parents[0]
except NameError:
    PROJECT_PATH = Path('.').absolute()
DATA_PATH = Path(PROJECT_PATH, 'data')

data_A = pd.read_feather(Path(DATA_PATH, 'cc_data_A.feather'))
data_A_immutable = data_A[['id', 'death', 'time']]
data_A_mutable = data_A.loc[:,'age':'antipsychotics']

with open(Path(PROJECT_PATH, "output_cc/A", "data_A_immutable.pkl"), 'wb') as f:
    pickle.dump(data_A_immutable, f)

with open(Path(PROJECT_PATH, "output_cc/A", "data_A_mutable.pkl"), 'wb') as f:
    pickle.dump(data_A_mutable, f)

data_B = pd.read_feather(Path(DATA_PATH, 'cc_data_B.feather'))
data_B_immutable = data_B[['id', 'death', 'time']]
data_B_mutable = data_B[['stage4']]

with open(Path(PROJECT_PATH, "output_cc/B", "data_B_immutable.pkl"), 'wb') as f:
    pickle.dump(data_B_immutable, f)
    
with open(Path(PROJECT_PATH, "output_cc/B", "data_B_mutable.pkl"), 'wb') as f:
    pickle.dump(data_B_mutable, f)

# %% DP
epsilon_list = [0.1, 0.5, 1, 10, 100, 1000, 10000]
epsilon = epsilon_list[0]

# %%
original_A = Original(data_A_mutable, ['sex', 'anxiolytic', 'antidepressant', 'antipsychotics']) 
original_B = Original(data_B_mutable, ['stage4']) 

# %%
diffprivacy_A = DiffPrivacy(original_A, "./output_cc/A")
diffprivacy_B = DiffPrivacy(original_B, "./output_cc/B")
# %%
for epsilon in epsilon_list:
    diffprivacy_A.dp(epsilon)
    diffprivacy_B.dp(epsilon)  
# %%
