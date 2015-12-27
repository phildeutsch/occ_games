<?php
    require_once("login.php");
    require_once("functions.php");
			
	$conn = new mysqli($host, $user, $pass, $db);
    if ($conn->connect_error) die($conn->connect_error);
	
	// check if player is already in DB
    $query = "SELECT count(*) FROM players
						   WHERE firstname = '$_POST[fname]'
						   and lastname = '$_POST[lname]'";
	$result = $conn->query($query);
	if(!$result) die($conn->error);

	$result->data_seek(0);
	$row = $result->fetch_array(MYSQLI_NUM);
    $count = $row[0];
	//echo $count;

	if ($count==0) {
		
		$email = strtolower($_POST['fname'] . "." . $_POST['lname'] . "@occstrategy.com");
		$query = "INSERT INTO players (firstname, lastname, elo, email) 
	    		  VALUES ('$_POST[fname]','$_POST[lname]', 1000, '$email')";
	    $conn->query($query);
	} else {
		// player already in the DB
		// TODO: Notify user and go back to previous page
	}
	
	header("Location: index.php");
	exit();
?>