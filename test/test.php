<?php header("Content-Type: text/html; charset=utf-8");
require_once('../core/php_python.php');
$res= ppython("test::go2", 1, 2, 'chen');
print_r($res);

?>
