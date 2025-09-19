# Digital Camouflage

Download the challenge pcap file. Use `tcp` as filter and then right click on any tcp packet and follow > TCP stream.
Change the stream to 3 and You will see userid and password. The password is `UEFwZHNqUlRhZQ%3D%3D`. This text looks like base64
encoded (Here %3D%3D means ==). 
Decode that base64 string and you'll get the flag.
