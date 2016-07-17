			<?php
        require_once("login.php");
        require_once("functions.php");

        $conn = new mysqli($host, $user, $pass, $db);
        if ($conn->connect_error) die($conn->connect_error);

				// sending query
				$query = "SELECT * FROM matches order by date_time desc limit 10";
        $result = $conn->query($query);
        if(!$result) die($conn->error);

        $rows = $result->num_rows;

        echo "<table><tr><th>Time</th><th>Id</th></tr>";
        for ($j = 0; $j < $rows; ++$j) {
          $result->data_seek($j);
          $row = $result->fetch_array(MYSQLI_ASSOC);

          //echo $row['firstname'] . ' ' . $row['lastname'] . ' ' . $row['elo'] . '<br>';
          echo "<tr><td>" . $row['date_time'] . "</td>";
          echo "<td>" . $row['id'] . "</td></tr>";
        }
        echo "</table>";


        $result->close();
        $conn->close();
			?>
