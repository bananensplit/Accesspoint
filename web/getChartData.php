<?php
$output = exec('sudo ../backend/getChartData.py -d 14');
header('Content-Type: application/json');
echo $output;
die(200);