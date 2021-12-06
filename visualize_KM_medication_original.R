library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
# read processed data
data <- arrow::read_feather(here('data/cc_data.feather')) %>% select(-id, -stage) 

medications <- c('anxiolytic', 'antidepressant', 'antipsychotics')

# survival analysis
for (medication_name in medications){
  medication <- data %>% select({{medication_name}}) %>% pull()

  model <- survfit(Surv(time, death) ~ medication, data=data)
  model

  # ggplot
  figure <- ggsurvplot(
    model,
    data = data,
    size = 1,                 # change line size
  #   palette = c("#E7B800", "#2E9FDF", "#6940A5"),# custom color palettes
    conf.int = TRUE,          # Add confidence interval
    pval = TRUE,              # Add p-value
    risk.table = TRUE,        # Add risk table
    risk.table.col = "strata",# Risk table color by groups
    legend.labs = c("non-Medication", "Medication"),    # Change legend labels
    risk.table.height = 0.25, # Useful to change when you have multiple groups
    ggtheme = theme_bw(),      # Change ggplot2 theme
    title = glue("{medication_name} - KM plot")
  )

  ggpubr::ggexport(figure, filename = here(glue('images/survival_{medication_name}.png')))
}
