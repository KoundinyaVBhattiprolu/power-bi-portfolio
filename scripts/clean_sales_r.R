# Clean messy_sales_raw.csv -> messy_sales_clean.csv
# Mirrors the R snippet in Koundinya's portfolio (dplyr + janitor).
# Run in R / RStudio with the working directory set to scripts/:
#   source("clean_sales_r.R")
library(dplyr)
library(janitor)
library(readr)
library(stringr)

sales_raw <- read_csv("../data/messy_sales_raw.csv", col_types = cols(.default = "c"))

sales_clean <- sales_raw %>%
  clean_names() %>%
  mutate(
    order_id = str_to_upper(str_trim(order_id)),
    # Revenue: strip ₹ and thousands separators; blank -> 0
    revenue = revenue %>%
      str_remove_all("₹") %>% str_remove_all(",") %>% str_trim() %>%
      as.numeric() %>% coalesce(0),
    # Dates: mixed DD/MM/YYYY and YYYY-MM-DD; unparseable -> NA, then dropped.
    # as.Date with tryFormats tries one format for the whole vector, so
    # parse each format explicitly and take the first that works per row.
    order_date = coalesce(
      as.Date(order_date, format = "%Y-%m-%d"),
      as.Date(order_date, format = "%d/%m/%Y")
    ),
    region = tools::toTitleCase(str_trim(region)),
    category = recode(category, "Electronic" = "Electronics"),
    quantity = as.numeric(quantity),
    channel = na_if(str_trim(channel), ""),
    channel = coalesce(channel, "Unknown"),
    product = str_trim(product)
  ) %>%
  filter(!is.na(order_date), quantity > 0) %>%
  distinct(order_id, .keep_all = TRUE) %>%
  arrange(order_date)

write_csv(sales_clean, "../data/messy_sales_clean.csv")
cat("Cleaned rows:", nrow(sales_clean), "\n")
print(head(sales_clean))
