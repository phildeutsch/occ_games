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
?>