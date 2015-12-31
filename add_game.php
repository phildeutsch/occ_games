        <?php
          require_once("login.php");
          require_once("functions.php");

          $conn = new mysqli($host, $user, $pass, $db);
          if ($conn->connect_error) die($conn->connect_error);

          // sending query
          $query = "SELECT * FROM players order by firstname desc";
          $result = $conn->query($query);  

          $rows = $result->num_rows;

          echo "<div class=\"container\">";
          echo "<div class=\"row\">";
          echo "<div id=\"gamebox\" class=\"col-lg-4\">";
          echo "<h3>Winning Team</h3>";

          // Player 1
          echo "<font color=\"white\">Select player one of winning team:</font><br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player1\" size=\"1\" color:#fff>";
          echo "<option class=resultsform value=\"0\">None</option>";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select><br><br>";

          // Player 2
          echo "<font color=\"white\">Select player two of winning team:</font><br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player2\" size=\"1\">";
          echo "<option value=\"0\">None</option>";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select><br><br>";
          echo "</div>"; // column
          echo "<div class=\"col-lg-4\"></div>";
          echo "<div id=\"gamebox\" class=\"col-lg-4\">";
          echo "<h3>Losing Team</h3>";

          // Player 3
          echo "<font color=\"white\">Select player one of losing team:</font><br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player3\" size=\"1\">";
          echo "<option value=\"0\">None</option>";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select><br><br>";

          // Player 4
          echo "<font color=\"white\">Select player two of losing team:</font><br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player4\" size=\"1\">";
          echo "<option value=\"0\">None</option>";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select><br><br>";

        echo "</div>"; // column
        echo "</div>"; // row
        echo "</div>"; // container
        
        echo "<br><br>";

        echo "<input type=\"submit\" value=\"Enter Game\">";
        echo "</form>";
        ?>
