require(RPostgreSQL)
require(dplyr)
require(tidyr)
require(RColorBrewer)
require(ggplot2)
require(gplots)

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "d13s5r5bpncpjb",
                 host = "localhost", port = 5432,
                 user = "awqniepdsmevdy", password = "NE2w2lY4s7lOBDWo0SdKiFbO8F")


players <- dbGetQuery(con, "SELECT id AS player_id, full_name AS player FROM tf_player")
teams <- dbGetQuery(con, "SELECT team_id, player_id FROM tf_team_players")
matches <- dbGetQuery(con, "SELECT match_id, team_id FROM tf_match_teams")
match_info <- dbGetQuery(con, "SELECT id AS match_id, played_date FROM tf_match")

matchdata = match_info %>%
  merge(matches, by="match_id") %>%
  merge(teams, by="team_id") %>%
  merge(players, by="player_id") %>%
  select(c(match_id, player))

matchdata = merge(matchdata, matchdata, by="match_id") %>%
  group_by(player.x, player.y) %>%
  summarise(
    n = n()
  ) %>%
  spread(player.y, n)

matchdata[is.na(matchdata)] = 0
matchdata = as.data.frame(matchdata)
rownames(matchdata) = matchdata$player.x
matchdata$player.x = NULL

heatmap.2(as.matrix(matchdata),
          cellnote = matchdata,  # same data set for cell labels
          # main = "Correlation", # heat map title
          notecol="black",      # change font color of cell labels to black
          density.info="none",  # turns off density plot inside color legend
          trace="none",         # turns off trace lines inside the heat map
          margins =c(13,15),     # widens margins around plot
          col=brewer.pal(9,"Blues"),       # use on color palette defined earlier 
          dendrogram="row",     # only draw a row dendrogram
          Rowv=TRUE,
          key=FALSE,
          Colv="Rowv")