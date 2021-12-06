library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
library(gtsummary)

# read processed data
data <- arrow::read_feather(here('data/cc_data.feather')) %>% select(-id, -stage) %>% mutate(across(c(-age, -time, -death), factor))

# coxph
  
regression_table <- summary(coxph(Surv(time, death) ~ age + sex + stage4 + antipsychotics + antidepressant + anxiolytic, data = data))
table_1 <- regression_table %>% 
                  .$coefficients %>% 
                  data.frame() %>% 
                  rownames_to_column('variable') %>%
                  select(variable, coef, HR = exp.coef., p = Pr...z..)
table_2 <- regression_table %>% 
                  .$conf.int %>% 
                  as_tibble() %>%
                  select(lowerCI = `lower .95`, upperCI = `upper .95` )
result <- bind_cols(table_1, table_2) %>% 
    select(variable, coef, HR, p, lowerCI, upperCI)

write_feather(result, here('output_cc/beta_original.feather'))
