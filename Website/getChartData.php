<?php
//$output = file_get_contents('../mothafuckingSampleData.json');
//$output = file_get_contents('../fuckingSampleData.json');
//$output = json_encode($output);
$output = '{"data":[';

$counter = 2;

for ($i = 0; $i < 100; $i++) {
    $output .= '{';
    $output .= '"utcDate": ' . (time() + 86000 * $i) * 1000 . ',';

    $uptime = rand(5, 24);
    $output .= '"raspberryUptime": ' . $uptime . ',';
    $output .= '"apUptime": ' . rand(0, $uptime) . ',';

    $output .= '"accesses": ' . random_int($counter, $counter + 40);
    $counter += 10;

    $output .= '},';
}

$output .= '{';
$output .= '"utcDate": ' . (time() + 86000 * $i) * 1000 . ',';

$uptime = rand(5, 24);
$output .= '"raspberryUptime": ' . $uptime . ',';
$output .= '"apUptime": ' . rand(0, $uptime) . ',';

$output .= '"accesses": ' . random_int($counter, $counter + 40);
$counter += 10;

$output .= '}]}';


header('Content-Type: application/json');

echo json_decode(json_encode($output));
die(200);