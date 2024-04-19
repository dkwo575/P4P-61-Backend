<?php


$servername = "localhost"; // server name(normally localhost
$username = "DoJunKwon"; // user name
$password = "smartfarm"; 
$database_name = "sensor_db";

$conn = mysqli_connect($servername, $username, $password, $database_name);

if (!$conn) {
	die("MySQL connection failed: " . mysqli_connect_error()); 
	
}

echo "Database connection is fine!";

if(isset($_POST ["temperature"]) && isset($_POST["humidity"]) ) {
	
	$temp = $_POST ["temperature"];
	$humi = $_POST["humidity"];
	//$light = $_POST["light"];
	//$wLevel = $_POST["waterLevel"];
	//$soilHumi = $_POST["soilHumidity"];
	//$steam = $_POST["steam"];
	// && isset($_POST["light"]) && isset($_POST["steam"])

	$sql = "INSERT INTO environments (temperature, humidity) VALUES (".$temp.", ".$humi." )";
//waterLevel, soilHumidity,   ".$wLevel.", ".$soilHumi.", , ".$light.", ".$steam." , light, steam
	if (mysqli_query($conn, $sql)) {
		echo "NEW record created successfully";
	} else {
		echo "Error: " . $sql . "<br>" . mysqli_error($conn);
	
	}
}




?>