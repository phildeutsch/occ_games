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

          $conn = new mysqli($host, $user, $pass, $db);
          if ($conn->connect_error) die($conn->connect_error);

          // sending query
          $query = "SELECT * FROM players order by firstname desc";
          $result = $conn->query($query);  

          $rows = $result->num_rows;

          echo "Select player 1:<br>";
          echo "<form method=\"post\" action=\"insert_game.php\">";
          echo "<select name=\"player1\" size=\"1\">";
          for ($j = 0; $j < $rows; ++$j) {
            $result->data_seek($j);
            $row = $result->fetch_array(MYSQLI_ASSOC);
            echo "<option value=\"" . $row['id'] . "\">" . 
              $row['firstname'] . " " . $row['lastname'] . "</option>";
          }
          echo "</select>";
        ?>
        <br><br>
        <input type="submit" value="Enter Game">
        </form>; 
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
