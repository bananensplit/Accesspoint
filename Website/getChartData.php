<?php
$output = file_get_contents('../mothafuckingSampleData.json');
//$output = file_get_contents('../fuckingSampleData.json');
$output = json_encode($output);
header('Content-Type: application/json');
echo json_decode($output);
die(200);