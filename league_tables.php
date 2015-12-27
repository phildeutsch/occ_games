<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>OC&C TF Portal</title>

    <!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="tf.css" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="index.php">OC&C TF Portal</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
    </nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <!-- <h1>Hello</h1>-->
        <br>
        <p>League tables </p>
<!--
    <p> <?php
      $python = `python python.py`;
      echo $python; ?>
    </p>
-->
      </div>
    </div>

		<div class="container">
		<p>
			<?php
        require_once("login.php");
        require_once("functions.php");

        $conn = new mysqli($host, $user, $pass, $db);
        if ($conn->connect_error) die($conn->connect_error);

				// sending query
				$query = "SELECT * FROM players order by elo desc";
        $result = $conn->query($query);
        if(!$result) die($conn->error);

        $rows = $result->num_rows;

        echo "<table><tr><th>Name</th><th>Score</th><th>Games</th></tr>";
        for ($j = 0; $j < $rows; ++$j) {
          $result->data_seek($j);
          $row = $result->fetch_array(MYSQLI_ASSOC);

          //echo $row['firstname'] . ' ' . $row['lastname'] . ' ' . $row['elo'] . '<br>';
          echo "<tr><td>" . $row['firstname'] . " " . $row['lastname'] . "</td>";
          echo "<td>" . $row['elo'] . "</td>";
          echo "<td>" . $row['games_played'] . "</td></tr>";
        }
        echo "</table>";


        $result->close();
        $conn->close();
			?>
		</p>
  </div>
  </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
