<?php
// エラーの出力
ini_set("display_errors", 1);
error_reporting(E_ALL);

// 保存先ディレクトリ
$_DIR = '/home/htdocs/snow_project/imgs/';

$fileID = random();

// save upload file
move_uploaded_file($_FILES['img']['tmp_name'], $_DIR.$fileID.'.png');

// return file ID
echo $fileID;




// ------------------------------- //
// ---------- functions ---------- //
// ------------------------------- //

// --- ランダムな文字列の生成 ---
function random($length = 8) {
    //$num = '0123456789';
    //$upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    //$lower = 'abcdefghijklmnopqrstuvwxyz';
    //$all = $num.$upper.$lower;
    //return substr(str_shuffle($all), 0, $length);
    return substr(str_shuffle('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), 0, $length);
}



?>
