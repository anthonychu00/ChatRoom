# Chatroom

Basic implementation of a chatroom using TCP/IP in Python using the command line.

1. First run server.py with a desired port number as an argument. The default IP Address for the server is localhost (127.0.0.1).
An example command would be (connecting to port 80):
$ python server.py 80

2. Then run client.py for each instance of a client you want to make, with IP Address and port number as arguments.
An example command would be (connecting to port 80 using localhost IP Address):
$ python client.py 127.0.0.1 80

3. On each client, you are prompted for a username that will be attached to the client. Just enter a string.

4. You are also given instructions while on the program on using some of the features in the program. 
Most importantly, you can see all active clients as a client by entering "?", and can send to a specific individual with ">".
For example:
Hi how are you > Joe
Send "Hi how are you" to a client associated with the name Joe, if one exists.

5. Press Ctrl + c to properly exit a client. To close the server just manually close the terminal window. 



* https://steelkiwi.com/blog/working-tcp-sockets/ was very helpful in figuring out what some of the boilerplate looked like
for implementing sockets in Python and providing the idea to use an infinite loop that blocks at certain points for the server and client.
