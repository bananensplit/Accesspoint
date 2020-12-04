<?php
$output = exec('/var/www/html/AccessPoint/accesspoint.py');
echo $output;
die(200);