import threading
import socket
import netifaces as ni

# Gets local machine address
# Holds Host IP and Port
class IPv4:
    def __init__(self):
        self.host = self.local_ip()  # Local Host 
        self.port = 12345            # Port isn't reserved so I chose it

    # Gets the name of your machine
    # Finds your IP from using your machines name
    def local_ip(self):
        # Get all network interfaces (keys from the interfaces dictionary)
        interfaces = ni.interfaces()
        
        # itr's through network interfaces
        for interface in interfaces:
            # Get all addresses for each interface
            addrs = ni.ifaddresses(interface)
            # Look for IPv4 addresses
            if ni.AF_INET in addrs:
                # Get the first IPv4 address
                # The first IP the system responds with is usually the main IP
                ipv4_info = addrs[ni.AF_INET][0]
                # the IP is found in the addr column
                address = ipv4_info['addr']
                # Check if the address is on the same subnet as your known IP
                if address.startswith('192.168.1.'):
                    return address
        # Fallback to localhost
        return '127.0.0.1'  
        
# Get port and machines IP 
ipv4 = IPv4()
host = ipv4.host
port = ipv4.port

# takes in an IP address and Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the server to the local host via port number
server.bind((host, port))

# Sets server on standby for incoming connections
server.listen()

# Lists of Clients and Usernames
clients = []
usernames = []

# Sending messages to the chatroom
def broadcast(message):
    for client in clients:
        client.send(message)

# Shows list of active users. Server console only
def users_list():
    print("Active Users: ")
    for user in usernames:
        print(user)
    print('\n')

# Manages clients and sends thier messages to chat
def handle(client):
    while True:
        try: 
            # Server recieving a message from a client to broadcast
            message = client.recv(1024).decode('ascii')

            # Check if the '!LEAVE' command is part of the message
            if '!LEAVE' in message:
                # Extract the username from the message
                username = message.split('!LEAVE')[0]

                # Outputs when someone left the chatroom
                broadcast(f'{username} has left the chat\n'.encode('ascii'))

                # Removes them from the list
                clients.remove(client)

                # Terminates connection to the client
                client.close()

                # Gets rid of username from the list
                usernames.remove(username)

                # Announce disconnection on the server console
                print(f'{username} has gracefully disconnected\n')

                # Displays remaining users
                users_list()
                break
            else:
                # Broadcast the message to all clients
                broadcast(message.encode('ascii'))

        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            # Attempt to cleanup the client's information

            break

# Recieving new clients
def recieve():
    # Stays true since we are always looking for new clients
    while True:
        # server is set open to accept clients
        client, address = server.accept()

        # send message to connecting client to enter a username
        client.send('Enter a username: '.encode('ascii'))

        # Gets username from client 
        username = client.recv(1024).decode('ascii')

        # Store usernames
        usernames.append(username)

        # Stores client
        clients.append(client)

        # Says which user connected
        print(f'{username} successfully connected to the server')
        
        # Says which address and port they connected to
        print(f'Connected from {str(address)}\n')

        # Displays updated user list
        users_list()

        # Displays to the entire chat that the new user has joined
        broadcast(f'{username} has joined the server!\n'.encode('ascii'))

        # Send to the user that they connected 
        client.send('You have successfully connected to the server\n'.encode('ascii'))

        # Creates a thread for the new client
        thread = threading.Thread(target=handle, args=(client,))

        # Activates thread
        thread.start()

# Server is open to reviece new clients
print('Host IP: ', host)
print("Server is listening . . .\n")
recieve()