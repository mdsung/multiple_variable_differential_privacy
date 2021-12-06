library(tidyverse)
library(arrow)
library(here)
library(glue)

counts = c('0', '10', '100', '1000', '10000')

# Read all count metric
read_metric_by_count <- function(count){
    data <- read_feather(here(glue('metric/epsilon_times_count{count}.feather'))) %>%
        mutate(count = count, .before = '0.1')

}

data <- counts %>% purrr::map_df(read_metric_by_count)
data
# Visualization
graph_data <- data %>% select(-`10000`) %>% filter(count != 0) %>%
    pivot_longer(cols = `0.1`:`1000`, names_to = 'epsilon', values_to = 'seconds') %>%
    group_by(count, epsilon) %>%
    summarize(mean_seconds = mean(seconds), 
            sd_seconds = sd(seconds),
            se_seconds = sd(seconds) / sqrt(n()),
            .groups = 'drop') %>%
    mutate(count = as.numeric(count)) %>%
    arrange(count, epsilon)


figure <- graph_data %>%
    ggplot(aes(epsilon, mean_seconds, color = count, group = count)) + 
        geom_line() +
        geom_point() +
        geom_errorbar(aes(ymin = mean_seconds - se_seconds, 
                          ymax = mean_seconds + se_seconds), 
                      width = 0.1) + 
        theme_classic()

ggsave(plot = figure, filename = here('images/time_metric_by_count_and_epsilon.png'), dpi = 300, height = 6, width = 8)

