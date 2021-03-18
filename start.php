<?php
if (isset($_POST['do'])) {
    exec('sudo ../backend/ap-control.py --' . $_POST['do']);
    die(200);
}