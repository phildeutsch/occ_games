require(RPostgreSQL)
require(dplyr)
require(dtplyr)
require(tidyr)
require(RColorBrewer)
require(ggplot2)
require(gplots)
require(data.table)
require(stringr)
require(lubridate)

start.of.week <- function(date) date - (setNames(c(6,0:5),0:6) [strftime(date,'%w')])

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "d13s5r5bpncpjb",
                 host = "localhost", port = 5432,
                 user = "awqniepdsmevdy", password = "NE2w2lY4s7lOBDWo0SdKiFbO8F")


match_info <- data.table(dbGetQuery(con, "SELECT id AS match_id, played_date FROM tf_match"))
match_info[, played_date:=as.Date(str_sub(played_date, 1L, 10))]

weekly_games = match_info %>%
  mutate(week = start.of.week(played_date)) %>%
  group_by(week) %>%
  summarize(
    games = n(),
    weekdays = length(unique(played_date)),
    start_date = min(played_date)
  ) %>%
  arrange(week)

ggplot(data=weekly_games) + theme_bw() + 
  geom_bar(aes(x=week, y=games), stat="identity")