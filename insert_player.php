<?php
    require_once("login.php");
    require_once("functions.php");

				
	$con = mysql_connect($host, $user, $pass);

	if (!mysql_connect($host, $user, $pass))
		die("Can't connect to database");

	if (!mysql_select_db($db))
		die("Can't select database");
	
	// check if player is already in DB
	$result = mysql_query("SELECT count(*) FROM players
						   WHERE firstname = '$_POST[fname]' and lastname = '$_POST[lname]'");
	if (!$result) {
		die("Query to show fields from table failed");
	}
	if (mysql_fetch_row($result)[0]==0) {
		// TODO: Send email to player and only enter them after they have confirmed
		$sql = "INSERT INTO players (firstname, lastname, elo) 
	    		VALUES ('$_POST[fname]','$_POST[lname]', 1000)";
		mysql_query($sql,$con);
	} else {
		// player already in the DB
		// TODO: Notify user and go back to previous page
	}
	
	header("Location: index.php");
	exit();
?>