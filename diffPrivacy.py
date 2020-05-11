import numpy as np
import pandas as pd
from copy import deepcopy
from scipy.stats import bernoulli
from sklearn.preprocessing import MinMaxScaler
from functools import partial

class diffPrivacy:
    def __init__(self, epsilon, df, DP_method):
        self.epsilon = epsilon
        self.method = DP_method
        self.check_df_variable_uniqueness(df)
        self.dimension = self.df.shape[1]
        self.user = self.df.shape[0] 
        self.make_norm_df()
        self.get_map_df_to_normdf()
        
        self.process()
            
    def check_df_variable_uniqueness(self, df):
        lst = []
        for i, column in enumerate(df):
            series = df[column]
            if len(set(series.to_list())) != series.shape[0]:
                lst.append(i)
        self.df = df.iloc[:,lst]
        
    def make_norm_df(self):
        self.min_max_scaler = MinMaxScaler()
        self.continuous_columns = self.df.describe().columns.to_list()
        self.categorical_columns = list(set(self.df.columns) - set(self.df.describe().columns))

        df_cat = self.categorical_to_onehot(self.df.filter(self.categorical_columns))
        self.df_cat_columns = df_cat.columns

        df_con = self.df.filter(self.continuous_columns)
        self.df = pd.concat([df_con, df_cat], axis = 1) 
        
        df_con = self.continuous_to_normalization(self.df.filter(self.continuous_columns))
        self.normdf = pd.concat([df_con, df_cat], axis = 1) 

    def get_map_df_to_normdf(self):
        self.map_df_to_normdf = {}         ## {0: [0], 1: [1], 2: [2], 3: [3], 4: [4, 5], 5: [6, 7], 6: [8], 7: [9, 10, 11, 12, 13, 14, 15, 16], 8: [17], 9: [18, 19]}
        for i, entity in enumerate(self.continuous_columns + self.categorical_columns):
            self.map_df_to_normdf[i] = [idx for idx,  col in enumerate(self.normdf.columns.to_list()) if entity in col]

    def process(self):
        self.k = int(max([1,min([self.dimension, np.floor(self.epsilon/2.5)])]))
        self.find_position_to_dp()
        
        # function 결정
        self.PM = partial(self.PM_value, epsilon = self.epsilon / self.k)
        self.HM = partial(self.HM_value, epsilon = self.epsilon / self.k)
        self.OUF = partial(self.optimized_unary_function, epsilon = self.epsilon / self.k)
        self.method_func = {
                    "PM": self.PM,
                    "HM": self.HM,
                    }
        
        self.new_df = deepcopy(self.normdf) 
        self.new_matrix = self.new_df.to_numpy()
        self.make_dp_df()
        self.new_df = pd.DataFrame(self.new_matrix, columns=self.normdf.columns)
        self.make_unnorm_dp_df()

    # DP method
    def PM_value(self, value, epsilon):
        x = np.random.rand()
        C = (np.exp(epsilon/2) + 1) / (np.exp(epsilon/2) - 1)
        l = (C+1)/2 * value - (C-1)/2
        r = l + C - 1
        x_threshold = np.exp(epsilon /2) / (np.exp(epsilon/2) + 1)
        if x < x_threshold:
            return (np.random.rand() * (r-l) + l)
        elif x >= x_threshold: 
            # double uniform distribution을 구현하지 못하여 기존의 uniform distribution을 transform 하여 구현
            ra = np.random.rand(1)[0] 
            ra_threshold = (r + C) / (r - l + 2*C)
            if ra < ra_threshold:
                return ra * (r - l + 2*C) - C
            else:
                return ra * (r - l + 2*C) - r + l - C
        
    def DM_value(self, value, epsilon):
        ##sample a Bernoulli variable 
        d = (np.exp(epsilon) + 1) / (np.exp(epsilon) - 1) 
        p = (((np.exp(epsilon) -1) / (2*np.exp(epsilon) +2)) * value) + 1/2
        u = bernoulli.rvs(size=1, p=p)[0]
        return d if u == 1 else (-1) * d

    def HM_value(self, value, epsilon):
        ## 논문에서 주어진대로 epsilon_star를 정의
        epsilon_star = np.log((-5 + 2 * ((6353 - 405 * np.sqrt(241)) ** (1/3)) + 2 * ((6353 + 405 * np.sqrt(241)) ** (1/3)))/27)    
        ## 논문에서 주어진대로 alpha를 정의
        alpha = 1 - np.exp(-epsilon / 2) if epsilon > epsilon_star else 0
        ## alpha가 동전의 Head가 나오는 확률로 coin에 H, T 결과가 나온다. 
        coin = np.random.choice(["H","T"], p = [alpha, 1-alpha])
        ## coin "H"일때 peicewise_method, "T"일 때 duchi를 실행시키는 것을 dictionary로 구현
        func_dict = {
                    "H": self.PM_value(value, epsilon), 
                    "T": self.DM_value(value, epsilon),
                    }        
        return func_dict[coin] 
    
    def optimized_unary_function(self, arr, epsilon):
        """
        input: encoded array, epsilon
        output: perturbed array
        """
        oue_p = 0.5
        oue_q = 1/(np.exp(epsilon) + 1)
        perturbation = {
                    1:bernoulli.rvs(size=1, p=oue_p).astype(np.uint8)[0],
                    0:bernoulli.rvs(size=1, p=oue_q).astype(np.uint8)[0],
                    }
        rst = [perturbation[a] for a in arr]
        return rst

    # Preprocessing
    def continuous_to_normalization(self, df_con):
        fitted = self.min_max_scaler.fit(df_con)
        df_con = self.min_max_scaler.transform(df_con)
        return pd.DataFrame(df_con, columns=self.continuous_columns)

    def continuous_to_invert_normalization(self, df_con, df_cat):
        df_con = self.min_max_scaler.inverse_transform(df_con)
        df_con = pd.DataFrame(df_con, columns = self.continuous_columns)
        self.new_unnorm_df = pd.concat([df_con, df_cat], axis = 1) 
        
    def categorical_to_onehot(self, df_cat):
        return pd.get_dummies(df_cat)

    #Processing
    def find_position_to_dp(self):
        self.position = np.zeros((self.user,self.k), dtype = np.int8)
        for i in range(self.user):
            self.position[i,]  = np.random.choice(self.dimension, self.k, replace=False)

    def calculate_each_row(self, r, c):        
        # want to remove for-loop → apply "apply" function in list
        # r row index
        # c column index
        continuous_func = self.method_func[self.method]
        categorical_func = self.OUF

        for column_index in c:
            target_column = self.map_df_to_normdf[column_index]
            columns = self.continuous_columns + self.categorical_columns 
            column_name = columns[column_index]
            
            if column_name in self.continuous_columns:
                if ~np.isnan(self.new_matrix[r, target_column[0]]):
                    self.new_matrix[r, target_column[0]] = continuous_func(self.new_matrix[r, target_column[0]])

            elif column_name in self.categorical_columns:
                category_value_list = [self.new_matrix[r, target_c] for target_c in target_column]
                result_list = categorical_func(category_value_list)
                for i, value in enumerate(result_list):
                    self.new_matrix[r, target_column[0] + i] = value

    def make_dp_df(self):
        for r, c in enumerate(self.position):
            self.calculate_each_row(r, c)
        
    def make_unnorm_dp_df(self):
        df_con = self.new_df.filter(self.continuous_columns)
        df_cat = self.new_df.filter(self.df_cat_columns)
        self.continuous_to_invert_normalization(df_con, df_cat)

