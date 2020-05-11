import pandas as pd 

def read_file(filename, id = False):
    if id:
        raw_dataframe = pd.read_csv(filename, index_col = 0)
    elif not id:
        raw_dataframe = pd.read_csv(filename)
    return raw_dataframe

def make_write_filename(read_filename, flag, epsilon):
    point_idx = read_filename.index(".")
    return f"{read_filename[:point_idx]}_{flag}_{epsilon}.csv"

def write_file(df, filename):
    df.to_csv(filename)
