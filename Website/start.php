<?php
if (isset($_POST['do']) && $_POST['do'] == 'start') {
    exec('sudo ../backend/ap-control.py 1');
    die(200);
} else if (isset($_POST['do']) && $_POST['do'] == 'stop') {
    exec('sudo ../backend/ap-control.py 0');
    die(200);
}