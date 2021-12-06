library(tidyverse)
library(arrow)
library(here)

original <- read_feather(here('output_cc/beta_original.feather'))
dp <- read_feather(here('output_cc/beta_by_epsilon.feather'))

original <- original %>% 
    mutate(variable = dplyr::recode(variable, 
                            "sex1" = "sex",
                            "stage41" = "stage4",
                            "antipsychotics1" = "antipyschotics",
                            "antidepressant1" = "antidepressant",
                            "anxiolytic1" = 'anxiolytic'))

dp <- dp %>% 
    mutate(variable = dplyr::recode(variable, 
                            "sex1" = "sex",
                            "stage41" = "stage4",
                            "antipsychotics1" = "antipyschotics",
                            "antidepressant1" = "antidepressant",
                            "anxiolytic1" = 'anxiolytic'))

target_variable <- 'sex'

original_HR <- original %>% filter(variable == target_variable) %>% pull(HR)
summary_data <- dp %>% 
    filter(variable == target_variable) %>%
    group_by(epsilon) %>% 
    summarize(mean_HR = mean(HR),
            sd_HR = sd(HR),
            se_HR = sd(HR) / n()) 

summary_data %>%
    ggplot(aes(x = epsilon, y = mean_HR)) + 
        geom_point() + 
        geom_errorbar(aes(ymax = mean_HR + se_HR, ymin = mean_HR - se_HR), width = 0.1) + 
        geom_hline(yintercept=age_original_HR, linetype = 'dashed') + 
        labs(x = "Epsilon", y = "HR", title = glue("{target_variable}_by_epsilon")) + 
        theme_classic()

dp %>% 
    filter(variable == target_variable) 
