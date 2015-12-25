<!DOCTYPE html>
<html lang="en">
   <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="index.php">OC&C TF Portal</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
    </nav>

  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Navbar Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="navbar.css" rel="stylesheet">
  </head>

  <body>

    <div class="container">
      <nav class="navbar navbar-light bg-faded">
        <button class="navbar-toggler hidden-sm-up" type="button" data-toggle="collapse" data-target="#navbar-header" aria-controls="navbar-header">
          &#9776;
        </button>
        <div class="collapse navbar-toggleable-xs" id="navbar-header">
          <a class="navbar-brand" href="#">Navbar</a>
          <ul class="nav navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Pricing</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
          </ul>
          <form class="form-inline pull-xs-right">
            <input class="form-control" type="text" placeholder="Search">
            <button class="btn btn-success-outline" type="submit">Search</button>
          </form>
        </div>
      </nav> <!-- /navbar -->

      <!-- Main component for a primary marketing message or call to action -->
      <div class="jumbotron">
<!--        <h1>.</h1> -->
        <p>Enter your game here.</p>
        <p> This does not work yet! </p>
      </div>


<div class="container">
		<p>
			<?php
				require_once("login.php");
				require_once("functions.php");

				$id1 = $_POST['player1'][0];
				$id2 = $_POST['player2'][0];
				$id3 = $_POST['player3'][0];
				$id4 = $_POST['player4'][0];

				echo "ID1: " . $id1 . "<br>";
				echo "ID2: " . $id2 . "<br>";
				echo "ID3: " . $id3 . "<br>";
				echo "ID4: " . $id4 . "<br>";

				// Check if there is at least one player per team
				if ($id1==0 && $id2==0) die("No player on winning team.");
				if ($id3==0 && $id4==0) die("No player on losing team.");

				// Check if a player is selected more than once
				$data   = array($id1, $id2, $id3, $id4);
				$data   = array_delete($data, 0);
				$unique = array_unique($data);
				if ( count($data) != count($unique) ) {
				  die("Each player can only play on one team.");
				}

				// Connect to DB
				$conn = new mysqli($host, $user, $pass, $db);
        		if ($conn->connect_error) die($conn->connect_error);

				// Enter match into matches table
        		$query = "INSERT INTO matches VALUES ()";
        		$result = $conn->query($query);
        		$query = "SELECT max(id) from matches";
        		$result = $conn->query($query);
				if(!$result) die($conn->error);
				$result->data_seek(0);
          		$row = $result->fetch_array(MYSQLI_NUM);
          		$match_id = $row[0];

				// Enter winners
				if ($id1>0) {
          			$query = "INSERT INTO winners (match_id, player_id) 
          					  VALUES ('$match_id', '$id1')";
          			$result = $conn->query($query);
        			if(!$result) die($conn->error);

        			echo "Player " . $id1 . " added as winner ";
        			echo "for match " . $match_id . ".<br>";
          		}
          		if ($id2>0) {
          			$query = "INSERT INTO winners (match_id, player_id) 
          					  VALUES ('$match_id', '$id2')";
          			$result = $conn->query($query);
        			if(!$result) die($conn->error);

        			echo "Player " . $id2 . " added as winner ";
        			echo "for match " . $match_id . ".<br>";
          		}

          		// Enter losers
				if ($id3>0) {
          			$query = "INSERT INTO losers (match_id, player_id) 
          					  VALUES ('$match_id', '$id3')";
          			$result = $conn->query($query);
        			if(!$result) die($conn->error);

        			echo "Player " . $id3 . " added as loser ";
        			echo "for match " . $match_id . ".<br>";
          		}
          		if ($id4>0) {
          			$query = "INSERT INTO losers (match_id, player_id) 
          					  VALUES ('$match_id', '$id4')";
          			$result = $conn->query($query);
        			if(!$result) die($conn->error);

        			echo "Player " . $id4 . " added as loser ";
        			echo "for match " . $match_id . ".<br>";
          		}

				// Update elo

			?>
		</p>
  </div>

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

