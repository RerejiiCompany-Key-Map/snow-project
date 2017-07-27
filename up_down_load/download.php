<?php

//画像のパスとファイル名
$fpath = 'pics/';

// 画像ファイル名(ID)の取得
$fname = $_GET['id'];
var_dump($_GET);
print($fname);
if (isset($fname) == FALSE) return;
$fname = $fname.'.png';

//画像のダウンロード
header('Content-Type: application/octet-stream');
header('Content-Length: '.filesize($fpath.$fname));
header('Content-disposition: attachment; filename="'.$fname.'"');
readfile($fpath.$fname);

?>