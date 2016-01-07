<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>OC&C TF Portal</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/tf.css" rel="stylesheet">

    <!-- SweetAlert -->
    <script src="js/sweetalert.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/sweetalert.css">

    <!-- Popup -->
    <script src="js/popup.js"></script>

</head>

<!-- The #page-top ID is part of the scrolling feature - the data-spy and data-target are part of the built-in Bootstrap scrollspy function -->

<body id="page-top" data-spy="scroll" data-target=".navbar-fixed-top">

    <!-- Navigation -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
            <div class="navbar-header page-scroll">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand page-scroll" href="#page-top">OC&C TF Portal</a>
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav">
                    <!-- Hidden li included to remove active class from about link when scrolled up past about section -->
                    <li class="hidden">
                        <a class="page-scroll" href="#page-top"></a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#table_single">League Table (Single)</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#table_team">League Table (Teams)</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Intro Section -->
    <section id="intro" class="intro-section">
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-12">
                    <!--
                    <h1>The OC&C TF Portal</h1>
                  -->
                </div>
            </div>
            <div class="row">
                <div class="col-xs-6">
                    <h2> Current Top 20 </h2>
                    <p> <?php include("league_tables.php"); ?> </p>
                </div>
                <div class="col-xs-6" id="recent_games">
                  <div>
                    <h2> Recent Matches </h2>
                    <p> <?php include("recent_matches.php"); ?> </p>
                  </div>
                  <div>
                      <h3> <br> </h2>

                        <p> <button onclick="myFunction()" class="btn"> Enter results</button></p>
                        <p> <button onclick="myFunction()" class="btn"> Enter player</button></p>
                        <p> <button onclick="myFunction()" class="btn"> Sign in</button></p>
                        <p> <button onclick="myFunction()" class="btn"> Contact</button></p>
                  </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="table_single" class="table-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>League Table (Single)</h1>
                </div>
                <p> <?php include("league_tables.php"); ?> </p>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="table_team" class="table-section">
      <div class="container">
          <div class="row">
              <div class="col-lg-12">
                  <h1>League Table (Team)</h1>
              </div>
              <p> <?php include("league_tables.php"); ?> </p>
          </div>
      </div>
  </section>

    <!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- Scrolling Nav JavaScript -->
    <script src="js/jquery.easing.min.js"></script>
    <script src="js/scrolling-nav.js"></script>

</body>

</html>
