<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Scrolling Nav - Start Bootstrap Template</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/tf.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

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
                        <a class="page-scroll" href="#table">League Table</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#results">Enter Results</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#player">Add Player</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Intro Section -->
    <section id="intro" class="intro-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>The OC&C TF Portal</h1>
                    <p>This page shows the current TF league table of the OC&C London office.</p>
                    <a class="btn btn-default page-scroll" href="#table">Show me the standings!</a>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="table" class="about-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>League Table</h1>
                </div>
                <p> <?php include("league_tables.php"); ?> </p>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="results" class="services-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>Enter Results</h1>
                </div>
            </div>
            <p> <?php include("add_game.php"); ?> </p>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="player" class="contact-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>Add Player</h1>
                </div>
            </div>
                          <p>
            <form action="insert_player.php" method="post">
                First name: <input type="text" id="fname" name="fname" /><br><br>
                Last name: <input type="text" id="lname" name="lname" /><br><br>
            <input type="submit" id="player-button" value="Add player">
            </form>

        </p>
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
