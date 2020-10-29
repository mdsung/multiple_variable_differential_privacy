import os.path
from typing import List

import numpy as np

from data import Original, Label, Data
import config
from utils import read_pkl_file, read_csv_file, get_categorical_levels_from_data

class Validation:
    def __init__(self, 
                epsilon:int, 
                original, 
                dp, 
                label, 
                train_size:float,
                epoch: int,):

        self.epsilon = epsilon
        self.original = original
        self.dp = dp

        self.original_data = original.data
        self.dp_data = dp.data
        self.label_data = label.data

        self.filter_category = original.filter_category
        self.filter_continuous = original.filter_continuous

        self.train_size = train_size
        self.epoch = epoch

    def process(self):
        self.category_result = self.categorical_validation(self.original_data, self.dp_data)
        self.continuous_result = self.continuous_validation(self.original_data, self.dp_data)
        self.model_result = self.model_validation(self.original_data, self.dp_data, self.label_data)

    def _get_misclassfication_rate(self, arr1, arr2):
        return 1 - np.isclose(arr1, arr2).sum(axis = 0)/ arr1.shape[0]

    def categorical_validation(self, original_data, dp_data):
        arr1 = original_data[:,self.filter_category]
        arr2 = dp_data[:,self.filter_category]
        return self._get_misclassfication_rate(arr1, arr2)

    def _get_mse(self, arr1, arr2):
        return np.sqrt(np.sum((arr1 - arr2) ** 2, axis = 0))

    def continuous_validation(self, original_data, dp_data):
        arr1 = original_data[:,self.filter_continuous]
        arr2 = dp_data[:,self.filter_continuous]
        return self._get_mse(arr1, arr2)

    def _add_classification_models(self):
        # from sklearn.linear_model import LogisticRegression
        # from sklearn.tree import DecisionTreeClassifier
        # from sklearn.neighbors import KNeighborsClassifier
        # from sklearn.naive_bayes import GaussianNB
        # from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        # self.classification_models.append(('Logistic Regression', LogisticRegression(solver="liblinear")))
        # self.classification_models.append(('K Nearest Neighbor', KNeighborsClassifier(n_neighbors=5, metric="minkowski",p=2)))
        # self.classification_models.append(('Kernel SVM', SVC(kernel = 'rbf',gamma='scale')))
        # self.classification_models.append(('Naive Bayes', GaussianNB()))
        # self.classification_models.append(('Decision Tree', DecisionTreeClassifier(criterion = "entropy")))
        self.classification_models.append(('Random Forest', RandomForestClassifier(n_estimators=100, criterion="entropy")))

    def _set_train_test_index(self):
        num_of_rows = self.original_data.shape[0]
        self.total_index = np.arange(num_of_rows)
        self.train_index = np.random.choice(self.total_index, int(np.floor(num_of_rows * self.train_size)), replace = False)
        self.test_index = np.setdiff1d(self.total_index, self.train_index)

    def model_validation(self, original_data, dp_data, label_data):
        self.classification_models = []
        self.metrics = []

        self._add_classification_models()
    
        for e in range(self.epoch):
            self._set_train_test_index()
            for name, model in self.classification_models:
                from sklearn.metrics import accuracy_score
                # from sklearn.metrics import roc_auc_score
                # from sklearn.metrics import precision_score
                # from sklearn.metrics import recall_score
                # from sklearn.metrics import f1_score

                # train dataset
                X_train = dp_data[self.train_index]
                Y_train = label_data[self.train_index]
                model.fit(X_train, Y_train)
                    
                # validation dataset
                X_test = original_data[self.test_index]
                Y_test = label_data[self.test_index]
                Y_pred = model.predict(X_test)

                metric_dict = {
                    "epoch": e,
                    "epsilon": self.epsilon,
                    "model": name,
                    #"roc_auc": roc_auc_score(Y_test, Y_pred),
                    "accuracy": accuracy_score(Y_test, Y_pred),
                    #"precision_score": precision_score(Y_test, Y_pred),
                    #"recall_score": recall_score(Y_test, Y_pred),
                    #"f1_score": f1_score(Y_test, Y_pred),
                    }
                self.metrics.append(metric_dict)

        return self.metrics

def main():
    filename = config.DP_CONFIG["filename"]
    filedir = config.DP_CONFIG["filedir"]
    full_file_path = os.path.join(filedir, filename)
    outputdir = config.DP_CONFIG["output_file_directory"]
    categorical_columns = config.DP_CONFIG["categorical_columns"]
    epsilon_list = config.DP_CONFIG["epsilon_list"]
    label_filename = config.DP_CONFIG["label_filename"]

    epsilon = epsilon_list[0]
    original = Original(filedir, filename, categorical_columns)
    dp = Data(epsilon, outputdir)
    label = Label(filedir, label_filename, original)

    validation = Validation(epsilon, original, dp, label, train_size = 0.8)
    validation.process()

    print(validation.category_result)
    print(validation.continuous_result)
    print(validation.model_result)

if __name__ == "__main__":
    main()
