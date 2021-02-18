<?php
$output = exec('../backend/getData.py');
header('Content-Type: application/json');
echo $output;
die(200);