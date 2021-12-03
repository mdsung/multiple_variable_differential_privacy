# %%
import re
import pandas as pd
from pathlib import Path
try:
    PROJECT_PATH = Path(__file__).parents[0]
except NameError:
    PROJECT_PATH = Path('.').absolute()
OUTPUT_A_PATH = Path(PROJECT_PATH, 'output_cc/A')
OUTPUT_B_PATH = Path(PROJECT_PATH, 'output_cc/B')
from utils import read_pkl_file

# %%
def create_dfs(path_:Path):
    immutable = read_pkl_file(list(path_.glob("*_immutable*"))[0])
    mutable = read_pkl_file(list(path_.glob("*_mutable*"))[0])
    epsilon_list = [f for f in path_.glob("*") if re.match('^[0-9.]+',f.stem)]
    dfs = {}
    for f in epsilon_list:
        data = read_pkl_file(f)
        data = pd.DataFrame(data, columns = mutable.columns)
        data = pd.concat([data, immutable], axis = 1)
        dfs[f.stem] = data
    return dfs

a_dfs = create_dfs(path_ = OUTPUT_A_PATH)
b_dfs = create_dfs(path_ = OUTPUT_B_PATH)
# %%
for epsilon in a_dfs.keys():
    data_a = a_dfs[epsilon]
    data_b = b_dfs[epsilon]
    data = pd.merge(data_a, data_b, on = ['id', 'death', 'time'])
    data.to_feather(Path(PROJECT_PATH, f'output_cc/cc_dp_{epsilon}.feather'))

# %%
