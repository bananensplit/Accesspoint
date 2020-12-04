<?php
if (isset($_POST['do']) && $_POST['do'] == 'start') {
    exec('sudo /var/www/html/AccessPoint/ap-control.py 0');
    die(200);
} else if (isset($_POST['do']) && $_POST['do'] == 'stop') {
    exec('sudo /var/www/html/AccessPoint/ap-control.py 1');
    die(200);
}