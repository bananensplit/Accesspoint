<?php
//$output = file_get_contents('../mothafuckingSampleData.json');
//$output = file_get_contents('../fuckingSampleData.json');
//$output = json_encode($output);
$output = '{"data":[';

for ($i = 0; $i < 100; $i++) {
    $output .= '{';
    $output .= '"utcDate": ' . (time() + 86000 * $i) * 1000 . ',';
    $output .= '"raspberryUptime": ' . rand(0, 24) . ',';
    $output .= '"apUptime": ' . rand(0, 24) . ',';
    $output .= '"accesses": ' . random_int(10, 100);
    $output .= '},';
}

$output .= '{';
$output .= '"utcDate": ' . (time() + 86000 * $i) * 1000 . ',';
$output .= '"raspberryUptime": ' . rand(0, 24) . ',';
$output .= '"apUptime": ' . rand(0, 24) . ',';
$output .= '"accesses": ' . random_int(10, 100);
$output .= '}]}';

header('Content-Type: application/json');

echo json_decode(json_encode($output));
die(200);