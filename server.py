import socket
import sys
import _thread as thread

MAX_CLIENTS = 10
# keeps track of list of clients using the server
active_clients = []
# use localhost IP Address
IP = "127.0.0.1"

# using port 80?
# checks number of command line arguments
if len(sys.argv) != 2:
    print("Please enter a port number.")
    exit()
port = int(sys.argv[1])

# sets up a server socket
# AF_INET indicates the types of addresses this socket can communicate with, in this case IPv4 addresses family
# The second argument is the socket type, SOCK_STREAM indicates it is a connection-based protocol (TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server lets OS know it will use this IP address and port, and binds them together
server.bind((IP, port))

# sets socket options
# first argument defines the protocol level of the option, SOL_SOCKET = socket level
# second argument specifies which option to set, in this case SO_REUSEADDR allows reuse of local addresses
# The third argument sets the option defined in the second argument to 1, which means it is active
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server is now listening for new connection requests
server.listen(MAX_CLIENTS)

print("Server started")


# starts a new thread to receives messages solely from this particular client
def client_thread(client, addr, username):
    # infinitely reads data from socket in batches of 1024 bytes
    while True:
        # receives message from client, recv() blocks until there is actually something to receive
        message = client.recv(4096)
        # ********sockets can only send and receive bytes,
        # so they need to be encoded and decoded for sending/receiving messages respectively
        decoded_message = message.decode()

        # if clients disconnect from other end with ctrl + c, disconnect and kill this client thread
        if not message:
            print("Uh oh, something went wrong with " + username + ". They might have quit.")
            disconnect(client)
            thread.exit()
        else:
            if decoded_message == "?":  # client asking for list of active_clients
                usernames = [c["user"] for c in active_clients]
                user_list = "Active users: " + str(usernames)
                encoded_user_list = user_list.encode()
                client.send(encoded_user_list)
            elif ">" in decoded_message:  # client wants to send to specific recipient
                arr = decoded_message.split(">")
                recipient = arr[1].strip()
                print("From user " + username + " : " + arr[0])
                print("Send to: " + recipient)
                send_one(arr[0], recipient, username, client)
            else:  # client is sending to all
                print("From user " + username + " : " + decoded_message)
                print("Send to all")
                send_all(decoded_message,  client, username)


# if the client hits ctrl-c, removes them from list of active clients
def disconnect(client):
    for connection in active_clients:
        if client is connection["sock"]:
            active_clients.remove(connection)
            print("Disconnected: " + connection["user"])


def send_all(message, client, user):
    to_send = user + " : " + message
    to_send_encoded = to_send.encode()
    for c in active_clients:
        if c["sock"] is not client:
            c["sock"].send(to_send_encoded)


def send_one(message, recipient, user, client):
    to_send = user + " : " + message
    to_send_encoded = to_send.encode()
    for c in active_clients:
        if recipient == c["user"] and c["sock"] is not client:
            c["sock"].send(to_send_encoded)


# constantly listens for new clients wanting to make a connection to the IP address and port
while True:

    # accept a new connection to this socket
    # conn is a new socket object that lets you send and receive data using the connection
    # address is the IP attached to the socket
    # socket.accept() blocks until a new client connects
    client_socket, address = server.accept()

    # when user client first registers, they are asked for a username, the server blocks until it receives one
    prompt = "Welcome! Please enter a username: "
    encoded_prompt = prompt.encode()
    client_socket.send(encoded_prompt)

    username = client_socket.recv(4096)
    decoded_username = username.decode()

    active_clients.append({"sock": client_socket, "user": decoded_username})
    print("New client connected: " + decoded_username)

    instructions = "End your message with > followed by a username to send to one person, \n" \
                   "otherwise it will be sent to everyone. \n" \
                   "If you want to see a list of active users, press ?"
    welcome = "Glad to have you here, " + decoded_username + "\n" + instructions + "\n"
    encoded_welcome = welcome.encode()
    client_socket.send(encoded_welcome)

    thread.start_new_thread(client_thread, (client_socket, address, decoded_username))
