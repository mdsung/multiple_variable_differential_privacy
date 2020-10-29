DP_CONFIG = {
    "filename": "X.csv", # input file name
    "filedir": "./data",      # input file directory
    "output_file_directory": "./outputs", # output file directory
    "categorical_columns": ["intubated",	
                        "vent",	
                        "dialysis", 
                        "eyes", 
                        "motor",
                        "verbal",
                        "meds",
                        ], # categorical column names
    "epsilon_list": [0.1, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000],
    "label_filename":"Y.csv",
    "train_size": 0.8, 
    "epoch":10,
}