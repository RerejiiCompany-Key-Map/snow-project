<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>view & download</title>
</head>

<body>

    <form action="" method="get">
        画像ID : 
        <?php
        $id = $_GET['id'];
        print '<input type="search" name="id" value="'.$id.'">';
        ?>
        <input type="submit" value="view">
    </form>
    </br>

    <?php
    $id = $_GET['id'];
    $filepath = 'imgs/'.$id.'.png';
    if (file_exists($filepath) == TRUE) {
        print '<img src="'.$filepath.'">';
        // CSSA
        print '<style type="text/css">';
        print '<!--';
        print 'img {
            max-width: 400px;
            max-height: 400px;
            }';
        print '-->';
        print '</style>';
        //print '<img src="'.$filepath.'">';
        print '</br>';
        print '<form action="download.php?id=output" method="get">';
        print '<input type="submit" value="Download">';
        print '<input type="hidden" name="id" value="'.$id.'">';
        print '</form>';
    } else {
        print 'The specified ID is not registered.';
    }
    ?>

</body>

</html>
