<?php
	function sanitizeString($var) {
		$var = stripsplashes($var);
		$var = strip_tags($var);
		$var = htmlentities($var);
		return $var;
	}

	function sanitizeMySQL($connection, $var) {
		$var = $connection->real_escape_string($var);
		$var = sanitizeString($var);
		return($var);
	}

	function array_delete($array, $element) {
    	return array_diff($array, [$element]);
    }

    function insert_winner($match_id, $player_id, $elo_change, $conn) {
    	$query = "INSERT INTO winners (match_id, player_id, elo_change) 
          		  VALUES ('$match_id', '$player_id', '$elo_change')";
        $result = $conn->query($query);
        if(!$result) die($conn->error);
        return 0;
    }

    function insert_loser($match_id, $player_id, $elo_change, $conn) {
    	$query = "INSERT INTO losers (match_id, player_id, elo_change) 
          		  VALUES ('$match_id', '$player_id', '$elo_change')";
        $result = $conn->query($query);
        if(!$result) die($conn->error);
        return 0;
    }

    function get_elo($player_id, $conn) {
    	if ($player_id > 0) {
	    	$query = "SELECT elo FROM players WHERE id = $player_id";
			$result = $conn->query($query);
	        if(!$result) die($conn->error);
	        $result->data_seek(0);
	        $row = $result->fetch_array(MYSQLI_NUM);
	        return $row[0];
	    } else {
	    	return 0;
	    }
    }

    // Elo calculation taken from https://en.wikipedia.org/wiki/Elo_rating_system
    function elo_change($r_a, $r_b, $K, $s) {
    	$e_a = 1 / (1 + pow(10, ($r_b-$r_a)/400));

    	$dr_a = $K * ($s - $e_a);
    	return $dr_a;
    }

    function update_elo($player_id, $elo_change, $conn) {
    		$query = "UPDATE players SET elo = elo + $elo_change
    				  WHERE id = $player_id";
			$result = $conn->query($query);
	        if(!$result) die($conn->error);
	        return 0;
    }

    function add_game($player_id, $conn) {
            $query = "UPDATE players SET games_played = games_played + 1
                      WHERE id = $player_id";
            $result = $conn->query($query);
            if(!$result) die($conn->error);
            return 0;
    }
?>