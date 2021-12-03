library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
library(gtsummary)

# read processed data
data <- arrow::read_feather(here('data/cc_data.feather')) %>% select(-id, -stage) 

# coxph
regression_table <- coxph(Surv(time, death) ~ age + sex + stage4 + antipsychotics + antidepressant + anxiolytic, data = data) %>% 
  gtsummary::tbl_regression(exp = TRUE) 
regression_table 
gt::gtsave(as_gt(regression_table), file = here('images/original_survival.png'))
