library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
library(gtsummary)
library(glue)
library(furrr)

future::plan('multicore', workers = 32)

# read processed data
create_regression_table_by_epsilon <- function(epsilon, attempt){
  data <- arrow::read_feather(here(glue('output_cc/{epsilon}_{attempt}.feather'))) %>% 
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
  result <- bind_cols(table_1, table_2) %>% tibble() %>%
    mutate(epsilon = epsilon, attempt = attempt) %>%
    select(attempt, epsilon, variable, coef, HR, p, lowerCI, upperCI) %>%
    mutate(variable = dplyr::recode(variable, 
                            "sex1" = "sex",
                            "stage41" = "stage4",
                            "antipsychotics1" = "antipyschotics",
                            "antidepressant1" = "antidepressant",
                            "anxiolytic1" = 'anxiolytic'))   
  return(result)
}

# create_regression_table_by_epsilon(epsilon, attempt)

epsilon_list = c("0.1", "1", "10", "100", "1000", "10000")
attempts = seq_along(1:50)

epsilon_attempt_list <- expand.grid(epsilon = epsilon_list, attempt = attempts)
result <- epsilon_attempt_list %>% furrr::future_map2_dfr(.x = .$epsilon, .y = .$attempt, .f = ~ create_regression_table_by_epsilon(.x, .y))

write_feather(result, 'output_cc/beta_by_epsilon.feather')
