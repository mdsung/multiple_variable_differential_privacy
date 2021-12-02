library(tidyverse)
library(arrow)
library(here)
library(survival)
library(survminer)
# read processed data
data <- arrow::read_feather(here('data/cc_data.feather')) %>% select(-id, -stage)

# survival analysis
model <- survfit(Surv(time, death) ~ stage4, data=data)
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
  legend.labs = c("non-Stage4", "Stage4"),    # Change legend labels
  risk.table.height = 0.25, # Useful to change when you have multiple groups
  ggtheme = theme_bw()      # Change ggplot2 theme
)

ggsave(plot=print(figure), 
    filename=here('images/survival_stage.pdf'))
