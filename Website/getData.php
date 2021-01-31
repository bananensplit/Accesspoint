<?php
$output = exec('../getData.py');
header('Content-Type: application/json');
echo $output;
die(200);