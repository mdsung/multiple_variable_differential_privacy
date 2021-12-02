from multiprocessing import Pool

from tqdm import tqdm
import config
from utils import write_pkl_file
from differential_privacy import DiffPrivacy
from data import Original, Label, Data
from validation import Validation

def main():
    # configurations
    filename = config.DP_CONFIG["filename"]
    filedir = config.DP_CONFIG["filedir"]
    outputdir = config.DP_CONFIG["output_file_directory"]
    categorical_columns = config.DP_CONFIG["categorical_columns"]
    epsilon_list = config.DP_CONFIG["epsilon_list"]
    label_filename = config.DP_CONFIG["label_filename"]
    train_size = config.DP_CONFIG["train_size"]
    epoch = config.DP_CONFIG["epoch"]

    original = Original(filedir, filename, categorical_columns)
    label = Label(filedir, label_filename, original)

    ## DP class 
    diffprivacy = DiffPrivacy(
        original,
        outputdir
    )

    # multiprocessing DP
    print("Get DP data...")
    # pool = Pool()
    # pool.map(diffprivacy.dp, epsilon_list)
    diffprivacy.dp(epsilon_list[0])
    
    # Validation
    # print("Start Get Metric...")
    # categorical_results = []
    # continuous_results = []
    # model_results = []
    
    # for epsilon in tqdm([0, *epsilon_list]):
    #     if epsilon == 0:
    #         validation = Validation(epsilon, original, original, label, train_size, epoch)
    #         validation.process()
    #         model_results.extend(validation.model_result)
    #         continue

    #     dp = Data(epsilon, outputdir)
    #     validation = Validation(epsilon, original, dp, label, train_size, epoch)
    #     validation.process()

    #     categorical_results.append(validation.category_result)
    #     continuous_results.append(validation.continuous_result)      
    #     model_results.extend(validation.model_result)

    # write_pkl_file(categorical_results, outputdir, "categorical_results.pkl")
    # write_pkl_file(continuous_results, outputdir, "continuous_results.pkl")
    # write_pkl_file(model_results, outputdir, "model_results.pkl")

if __name__ == "__main__":
    main()