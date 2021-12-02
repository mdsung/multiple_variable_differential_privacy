library(tidyverse)
library(arrow)
library(here)

data <- read_csv(here('data/final_data1104_1.csv'), locale=locale('ko',encoding='euc-kr'))
stage <- read_csv(here('data/stage.csv'), locale=locale('ko',encoding='euc-kr'))

# select columns
preprocessed_data <- data %>%   
    left_join(stage, by = '실명_등록번호') %>%
    select(id = 실명_등록번호, age = age_diag, sex, stage, sum_A, sum_P, sum_D, psymed, death, time = 생존기간) 

# data recode
preprocessed_data <- preprocessed_data %>%
    mutate(stage = recode(stage, '0' = 1))

# data type
preprocessed_data <- preprocessed_data %>% 
    mutate(sex = factor(sex)) %>%
    mutate(stage4 = factor(ifelse(stage == 4, 1, 0))) %>%
    mutate(stage = factor(stage)) 


# save file to feather
arrow::write_feather(preprocessed_data, here('data/cc_data.feather'))
