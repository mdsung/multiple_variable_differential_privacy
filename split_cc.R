library(tidyverse)
library(arrow)
library(here)

# read processed data
data <- arrow::read_feather(here('data/cc_data.feather')) 

data_A <- data %>% select(id, age, sex, anxiolytic, antidepressant, antipsychotics, death, time) %>% na.omit()

data_B <- data %>% select(id, stage4, death, time) %>% na.omit()

write_feather(data_A, here('data/cc_data_A.feather'))
write_feather(data_B, here('data/cc_data_B.feather'))
