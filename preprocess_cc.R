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
    mutate(stage = recode(stage, '0' = 1)) %>%
    mutate(sex = recode(sex, 'M' = 1, "F" = 0)) %>%
    mutate(stage4 = ifelse(stage == 4, 1, 0), .after = 'stage') %>%
    mutate(antipsychotics = ifelse(sum_P >= 7, 1, 0), .after = 'psymed') %>%
    mutate(antidepressant = ifelse(sum_D >= 7, 1, 0), .after = 'psymed') %>%
    mutate(anxiolytic = ifelse(sum_A >= 7, 1, 0), .after = 'psymed') 

# fill na
preprocessed_data <- preprocessed_data %>%
    mutate(antipsychotics = replace_na(antipsychotics, 0)) %>%
    mutate(antidepressant = replace_na(antidepressant, 0)) %>%
    mutate(anxiolytic = replace_na(anxiolytic, 0)) 

# data type
preprocessed_data <- preprocessed_data %>% 
    mutate(sex = factor(sex)) %>%
    mutate(stage = factor(stage)) %>%
    mutate(stage4 = factor(stage4)) %>%
    mutate(across(starts_with("anti"), factor)) %>%
    mutate(anxiolytic = factor(anxiolytic)) 

# drop column
preprocessed_data <- preprocessed_data %>% select(-stage) 

# save file to feather
arrow::write_feather(preprocessed_data, here('data/cc_data.feather'))
