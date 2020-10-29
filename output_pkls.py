import os.path
import pickle

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import config
from data import Original

filename = config.DP_CONFIG["filename"]
filedir = config.DP_CONFIG["filedir"]
outputdir = config.DP_CONFIG["output_file_directory"]
categorical_columns = config.DP_CONFIG["categorical_columns"]
epsilon_list = config.DP_CONFIG["epsilon_list"]
label_filename = config.DP_CONFIG["label_filename"]

files = ["categorical_results.pkl", 
        "continuous_results.pkl",
        "model_results.pkl"]

original = Original(filedir, filename, categorical_columns)

results = []
for i, file in enumerate(files):
    full_file_name = os.path.join("./outputs", file)
    with open(full_file_name, "rb") as f:
       results.append(pickle.load(f))

epsilon_df = pd.DataFrame({"epsilon":epsilon_list})
categorical_metric_df = pd.concat([epsilon_df, pd.DataFrame(results[0], columns= original.categorical_columns)])
continuous_metric_df =pd.concat([epsilon_df, pd.DataFrame(results[1], columns= original.continuous_columns)])
model_metric_df = pd.DataFrame(results[2])

fig = plt.figure()
categorical_metric_df.plot()
plt.show()