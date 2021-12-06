library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
library(gtsummary)
library(glue)
library(furrr)

future::plan("multicore", workers = 30)
epsilon_list = c('0.1', '0.5', '1', '10', '100', '1000', '10000')

# read processed data
create_regression_table_by_epsilon <- function(epsilon){
  data <- arrow::read_feather(here(glue('output_cc/cc_dp_{epsilon}.feather'))) %>% 
      select(-id) %>%
      mutate(across(c(-age, -time, -death), factor))
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
    mutate(epsilon = epsilon, .before='coef') %>%
    select(variable, epsilon, coef, HR, p, lowerCI, upperCI)
    
  return(result)
}

create_regression_table <- function(attempt){
  result <- epsilon_list %>% map_df(create_regression_table_by_epsilon)
  result <- result %>% dplyr::mutate(attemp = attempt, .before='variable')
  return(result)
}

result_table <- seq_along(1:100) %>% 
  furrr::future_map_dfr(create_regression_table)

write_feather(result_table, here('data/beta_by_epsilon.feather'))

