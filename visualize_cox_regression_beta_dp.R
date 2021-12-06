library(tidyverse)
library(arrow)
library(here)
library(glue)
library(tools)

original <- read_feather(here('output_cc/beta_original.feather'))
dp <- read_feather(here('output_cc/beta_by_epsilon.feather'))

original_variable <- original %>% select(variable, original_HR = HR)

summary_data <- dp %>% 
    group_by(variable, epsilon) %>% 
    summarize(mean_HR = mean(HR),
            sd_HR = sd(HR),
            se_HR = sd(HR) / n(), .groups = 'drop') %>%
    left_join(original_variable) %>%
    mutate(variable = factor(variable, levels = c('age', 'sex', 'stage4', 'antipsychotics', 'antidepressant', 'anxiolytic')))


HR_figure <- summary_data %>%
    ggplot(aes(x = epsilon, y = mean_HR)) + 
        geom_point() + 
        geom_errorbar(aes(ymax = mean_HR + sd_HR, ymin = mean_HR - sd_HR), width = 0.1) + 
        geom_hline(aes(yintercept = original_HR), linetype = 'dashed', color = 'red') + 
        labs(x = "Epsilon", y = "HR", title = "Cox regression HR by Epsilon in Vertical Partitioned Data")+ 
        theme_classic() + 
        facet_wrap(~variable, scales = 'free_y')

ggsave(plot = HR_figure, filename = here('images/HR_by_epsilon.png'), height = 8, width = 8, dpi = 300)

