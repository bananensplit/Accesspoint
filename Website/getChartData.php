<?php
$output = exec('sudo ../backend/getChartData.py');
header('Content-Type: application/json');
echo json_decode(json_encode($output));
die(200);