<?php


$servername = "localhost"; // server name(normally localhost
$username = "DoJunKwon"; // user name
$password = "smartfarm"; // replace your mysql password
$database_name = "sensor_db"; // replace your datatbase name // sensor_db

$conn = mysqli_connect($servername, $username, $password, $database_name);

if (!$conn) {
	die("MySQL connection failed: " . mysqli_connect_error()); 
	
}

echo "Database connection is fine!";

// Handle HTTP POST request from ESP32
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Extract sensor data (modify as needed)
    $temperature = $_POST["temperature"];
    $humidity = $_POST["humidity"];
	$light = $_POST["light"];
	$waterLevel = $_POST["WaterLevel"]; //isset($_POST["waterLevel"]) ? $_POST["waterLevel"]:'1'; 
	$soilHumidity = $_POST["SoilHumidity"]; //isset($_POST["soilHumidity"]) ? $_POST["soilHumidity"]:'2';
	$steam =  $_POST["Steam"]; // isset($_POST["steam"]) ? $_POST["steam"]:'3';
	
	 // Insert data into MySQL table
    $sql = "INSERT INTO real_iot (temperature, humidity, light, waterLevel, soilHumidity, steam) VALUES ('$temperature', '$humidity', '$light', '$waterLevel', '$soilHumidity', '$steam')";
	//$sql = "INSERT INTO environments (temperature, humidity, light, waterLevel, soilHumidity, steam) VALUES ('$temperature', '$humidity', '$light', '$waterLevel', '$soilHumidity', '$steam')"; change table name
	if ($conn->query($sql) === TRUE) {
        echo "Data inserted successfully!";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();

/*
if(isset($_POST["temperature"]) && isset($_POST["humidity"]) && isset($_POST["light"]) && isset($_POST["waterLevel"]) && isset($_POST["soilHumidity"]) && isset($_POST["steam"]) ) {
	
	$temp = $_POST["temperature"];
	$humi = $_POST["humidity"];
	$lightV = $_POST["light"];
	$wLevel = $_POST["waterLevel"];
	$soilHumi = $_POST["soilHumidity"];
	$steamV = $_POST["steam"];
	
	// && isset($_POST["light"]) && isset($_POST["steam"])

	$sql = "INSERT INTO environments (temperature, humidity, light, waterLevel, soilHumidity, steam) VALUES (".$temp.", ".$humi.", ".$lightV.", ".$wLevel.", ".$soilHumi.", ".$steamV.")";
//waterLevel, soilHumidity,   ".$wLevel.", ".$soilHumi.", , ".$light.", ".$steam." , light, steam
	if (mysqli_query($conn, $sql)) {
		echo "NEW record created successfully";
	} else {
		echo "Error: " . $sql . "<br>" . mysqli_error($conn);
	
	}
}

*/

?>