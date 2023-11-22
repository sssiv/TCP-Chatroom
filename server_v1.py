import threading
import socket
from ip import IPv4 
        
# Get port and machines IP 
ipv4 = IPv4()
host = ipv4.host
port = ipv4.port

# takes in an IP address and Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associates the server with a specific network interface/port number on the host machine. 
# This is necessary for the server to receive incoming network requests on that port.
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

                # Outputs to all clients when someone left the chatroom
                broadcast(f'{username} has left the chat\n'.encode('ascii'))

                # Removes client from the list
                clients.remove(client)

                # Terminates connection to the client
                client.close()

                # Removes the clients username from the list
                usernames.remove(username)

                # Announce disconnection on the server console
                print(f'{username} has gracefully disconnected\n')

                # Displays remaining users
                users_list()
                break
            else:
                # Broadcast recieved message to all clients
                broadcast(message.encode('ascii'))

        except Exception as e:
            # Display error code/status
            print(f"An error occurred: {e}")

            # Terminate Client connection
            client.close()
            break

# Recieving new clients, make Threads
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

if __name__ == "__main__":
    # Server is open to reviece new clients
    print('Host IP: ', host)
    print('Server v1 is now active\n')
    recieve()