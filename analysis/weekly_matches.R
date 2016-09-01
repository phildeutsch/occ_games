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
require(RJDBC)

start.of.week <- function(date) date - (setNames(c(6,0:5),0:6) [strftime(date,'%w')])

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "d13s5r5bpncpjb",
                 host = "localhost", port = 5432,
                 user = "awqniepdsmevdy", password = "NE2w2lY4s7lOBDWo0SdKiFbO8F")

# library(DBI)
# library(RPostgres)
# con <- dbConnect(RPostgres::Postgres(),dbname = 'd13s5r5bpncpjb', 
#                  host = 'ec2-54-75-238-7.eu-west-1.compute.amazonaws.com', # i.e. 'ec2-54-83-201-96.compute-1.amazonaws.com'
#                  port = 5432, # or any other port specified by your DBA
#                  user = 'awqniepdsmevdy',
#                  password = 'NE2w2lY4s7lOBDWo0SdKiFbO8F')

match_info <- data.table(dbGetQuery(con, "SELECT id AS match_id, matchtype, played_date FROM tf_match"))
match_info[, played_date:=as.Date(str_sub(played_date, 1L, 10))]
match_info[, matchtype:=relevel(factor(matchtype), "NA")]

weekly_games = match_info %>%
  mutate(week = start.of.week(played_date)) %>%
  group_by(week, matchtype) %>%
  summarize(
    games = n(),
    weekdays = length(unique(played_date)),
    start_date = min(played_date)
  ) %>%
  arrange(week, matchtype)

ggplot(data=weekly_games) + theme_bw() + 
  geom_bar(aes(x=week, y=games, fill=matchtype), stat="identity") +
  scale_fill_manual(values=c("#999999", "#9ecae1", "#3182bd"))
