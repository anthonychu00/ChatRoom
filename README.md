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

Code Description:

When server.py is started, it creates a socket using the socket library, binds it to an IP (localhost) and
port number, and starts listening for clients. It also allows for reuse of the IP Address used for making the server
through setsockopt(). Server.py then runs in an infinite while loop, blocking at socket.accept() to await requests from
new clients.

Similarly, when client.py is started, the client creates a socket and attempts to connect with socket.connect() at the 
specified port number, which will succeed since server.py is awaiting connection requests in it's while loop. The 
server asks for a username from the client and adds the client object - username mapping to a list that keeps track of
the active clients. The server then finally starts a thread with the function client_thread that listens for messages 
from that particular client in its own infinite while loop, blocking at socket.recv() until a client sends a message.

The server analyzes the contents of the message, looking for special characters "?" and ">" of which it will do one
of four things depending on if a special character was detected:

"?" - sends requesting client a list of active users using socket.send()

".*> recipient" - sends message to appropriate recipient with send_one(), selecting the appropriate client from the 
username mapping

"" - no special character, so defaults to function send_all()

SIGINT - client has disconnected most likely, run disconnect() to remove that client from list of active clients,
and notify the remaining clients. 

Meanwhile client.py executes it's own infinite while loop, listening for input from the user or server. A combination
of the select and msvcrt libraries was used to achieve this. With select handling server input and msvcrt handling
user input through detecting if the user has begun typing. Depending on the type of input the client will print to 
it's own terminal or send the input to the server to be printed to other terminals. For more details check the 
corresponding comments. 

This goes on until a client decides to disconnect by hitting CTRL + C (SIGINT) to exit. I would have liked the client
to implement a signal handler for SIGINT to properly close the socket, but that's a limitation of
programming on a Windows machine. This limitation of not being able to implement signal handlers at the system level 
also prevents the server.py code from breaking out of it's infinite loop with CTRL + C, so you have to close the 
terminal window manually. 

* This code was tested on a Windows machine. It might not work on a Linux or Mac machine since the Windows command prompt has 
different functionality. I'm not sure if msvcrt will cause problems in other terminals.

* https://steelkiwi.com/blog/working-tcp-sockets/ was very helpful in figuring out what some of the boilerplate looked like
for implementing reading and writing from sockets in Python, and providing the idea to use an infinite loop that blocks at certain points for the server and client.
