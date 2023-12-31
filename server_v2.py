# Differnece from V1:
#   * Uses a map to hold clients
#   * Each client is mapped with their IP and username


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

# Map{Key = Clients, value = Usernames}
clients_usernames_map = {}

# Add new client mapped to their username
def new_client(key, value):
    clients_usernames_map[key] = value

# Pass in client object to just delete from map
def remove_client(key):
    del clients_usernames_map[key]

# Displays messages sent from a client to all the clients
def broadcast(message):
    for client in clients_usernames_map.keys():
        client.send(message)

# List of connected clients
def users_list():
    print("Active Users: ")
    for username in clients_usernames_map.values():
        print(username)
    print('\n')    

# This runs when recieving messages from clients
# When there are no messages being sent, the function doesnt run
# But when the leave keyword is used,
# it handles disconnecting the said client
def handle(client):
    threading = True
    while threading:
        try:
            # Server recieving a message from a client to broadcast
            message = client.recv(1024).decode('ascii')

            # Check if the '!LEAVE' command is part of the message
            if message == '!LEAVE':
                # get username
                username = clients_usernames_map[client]

                # Outputs to all clients when someone left the chatroom
                broadcast(f'{username} has left the chat\n'.encode('ascii'))

                # Removes Client and Username from the map
                remove_client(client)

                # Terminate leaving clients connection
                client.close()
                print(f'{username} has gracefully disconnected\n')

                # Display current clients to the server
                users_list()
                threading = False
                break
            else:
                # Broadcast recieved message to all clients
                broadcast(message.encode('ascii'))

        except Exception as e:
            # Display Error code/status
            print(f"An error occurred: {e}")

            # Terminates Client connection
            client.close()

            # Checks if client is still in the map
            if client in clients_usernames_map:
                # Tell the chat they left unexpectedly
                print(f"{clients_usernames_map[client]} has unexpectedly disconnected")
                
                # Then remove them from the map
                remove_client(client)

            # Set running flag to off
            threading = False
            break

# Recieve new Client connections, make Threads
def receive():
    while True:
        # Accept client connection
        client, address = server.accept()

        # Prompt new client to enter in a username
        client.send('Enter a username: '.encode('ascii'))

        # Username from the client
        username = client.recv(1024).decode('ascii')

        # Maps new client with username
        new_client(client, username)

        # Displays connection success
        print(f'{username} successfully connected to the server')
        print(f'Connected from {str(address)}\n')

        # Displays all connected clients
        users_list()

        # Tells all clients the new client has joined
        broadcast(f'{username} has joined the server!\n'.encode('ascii'))

        # Sends a message to the client saying they have connected
        client.send('You have successfully connected to the server\n'.encode('ascii'))

        # Thread made for new client
        thread = threading.Thread(target=handle, args=(client,))

        # Start runnning Thread
        thread.start()

if __name__ == "__main__":
    print('Host IP: ', host)
    print('Server v2 is now active\n')
    receive()