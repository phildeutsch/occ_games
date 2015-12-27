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
				echo "<br>";

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

        // Get Elo ratings
        $elo1 = get_elo($id1, $conn);
        $elo2 = get_elo($id2, $conn);
        $elo3 = get_elo($id3, $conn);
        $elo4 = get_elo($id4, $conn);

    //  		echo "Elo 1: " . $elo1 . "<br>";
    //  		echo "Elo 2: " . $elo2 . "<br>";
    //  		echo "Elo 3: " . $elo3 . "<br>";
    //  		echo "Elo 4: " . $elo4 . "<br>";
				// echo "<br>";


     		if ($id1 > 0 && $id2 > 0) {
     			$elo_winners = ($elo1 + $elo2) / 2;
     		} else {
     			$elo_winners = max(array($elo1, $elo2));
     		}
     		if ($id3> 0 && $id4 > 0) {
     			$elo_losers = ($elo3 + $elo4) / 2;
     		} else {
     			$elo_losers = max(array($elo3, $elo4));
     		}

     		// echo "Elo winners: " . $elo_winners . "<br>";
     		// echo "Elo losers: " . $elo_losers . "<br>";
     		// echo "<br>";

				// Enter winners and update elo
				if ($id1>0) {
					$delo = elo_change($elo_winners, $elo_losers, 32, 1);
          insert_winner($match_id, $id1, $delo, $conn);
          update_elo($id1, $delo, $conn);
          add_game($id1, $conn);

        // 	echo "Player " . $id1 . " added as winner ";
        // 	echo "for match " . $match_id . ".<br>";
     			// echo "Elo change: " . $delo . "<br>";
     		}
     		if ($id2>0) {
  				$delo = elo_change($elo_winners, $elo_losers, 32, 1);
     			insert_winner($match_id, $id1, $delo, $conn);
     			update_elo($id2, $delo, $conn);
          add_game($id2, $conn);

     			// echo "Player " . $id2 . " added as winner ";
     			// echo "for match " . $match_id . ".<br>";
     			// echo "Elo change: " . $delo . "<br>";
     		}

     		// Enter losers
				if ($id3>0) {
  				$delo = elo_change($elo_losers, $elo_winners, 32, 0);
     			insert_winner($match_id, $id3, $delo, $conn);
     			update_elo($id3, $delo, $conn);
          add_game($id3, $conn);

     		// 	echo "Player " . $id3 . " added as loser ";
     		// 	echo "for match " . $match_id . ".<br>";
    			// echo "Elo change: " . $delo . "<br>";
       		}
     		if ($id4>0) {
  				$delo = elo_change($elo_losers, $elo_winners, 32, 0);
     			insert_winner($match_id, $id4, $delo, $conn);
     			update_elo($id4, $delo, $conn);
          add_game($id4, $conn);

     			// echo "Player " . $id4 . " added as loser ";
     			// echo "for match " . $match_id . ".<br>";
     			// echo "Elo change: " . $delo . "<br>";
     		}

            header('Location: index.php#table')
			?>