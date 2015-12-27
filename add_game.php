        <?php
          require_once("login.php");
          require_once("functions.php");

          $conn = new mysqli($host, $user, $pass, $db);
          if ($conn->connect_error) die($conn->connect_error);

          // sending query
          $query = "SELECT * FROM players order by firstname desc";
          $result = $conn->query($query);  

          $rows = $result->num_rows;

          // Player 1
          echo "Select player one of winning team:<br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player1\" size=\"1\">";
          echo "<option value=\"0\">None</option>";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select><br><br>";

          // Player 2
          echo "Select player two of winning team:<br>";
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

          // Player 3
          echo "Select player one of losing team:<br>";
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
          echo "Select player two of losing team:<br>";
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
        
        echo "<br><br>";
        echo "<input type=\"submit\" value=\"Enter Game\">";
        echo "</form>";
        ?>
