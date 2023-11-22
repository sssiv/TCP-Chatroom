# Difference from V2:
#   * Server functions are now in a class
#   * The socket is made and bind when a server object instance is made
#   * run() is now the function to run the server instead of recieve()

import socket
import threading
from ip import IPv4
    
class Server:
    def __init__(self, port=12345):
        self.host = IPv4().local_ip()
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients_usernames_map = {}
        self.ip = IPv4()

    def new_client(self, key, value):
        self.clients_usernames_map[key] = value

    def remove_client(self, key):
        del self.clients_usernames_map[key]

    # Send recieved message to all clients
    def broadcast(self, message):
        for client in self.clients_usernames_map.keys():
            client.send(message)

    # Print active users
    def users_list(self):
        print("Active Users: ")
        for username in self.clients_usernames_map.values():
            print(username)
        print('\n')    

    # Used for getting and removing clients
    def handle(self, client):
        threading = True
        while threading:
            try:
                # Server recieving a message from a client to broadcast
                message = client.recv(1024).decode('ascii')

                # Check if the '!LEAVE' command is part of the message
                if message == '!LEAVE':
                    # get username
                    username = self.clients_usernames_map[client]

                    # Outputs to all clients when someone left the chatroom
                    self.broadcast(f'{username} has left the chat\n'.encode('ascii'))

                    # Removes Client and Username from the map
                    self.remove_client(client)

                    # Terminate leaving clients connection
                    client.close()
                    print(f'{username} has gracefully disconnected\n')

                    # Display current clients to the server
                    self.users_list()
                    threading = False
                    break
                else:
                    # Broadcast recieved message to all clients
                    self.broadcast(message.encode('ascii'))

            except Exception as e:
                # Display Error code/status
                print(f"An error occurred: {e}")

                # Terminates Client connection
                client.close()

                # Checks if client is still in the map
                if client in self.clients_usernames_map:
                    # Tell the chat they left unexpectedly
                    print(f"{self.clients_usernames_map[client]} has unexpectedly disconnected")
                    
                    # Then remove them from the map
                    self.remove_client(client)

                # Set running flag to off
                threading = False
                break

    def receive(self):
        while True:
            # Accept client connection
            client, address = self.server.accept()

            # Prompt new client to enter in a username
            client.send('Enter a username: '.encode('ascii'))

            # Username from the client
            username = client.recv(1024).decode('ascii')

            # Maps new client with username
            self.new_client(client, username)

            # Displays connection success
            print(f'{username} successfully connected to the server')
            print(f'Connected from {str(address)}\n')

            # Displays all connected clients
            self.users_list()

            # Tells all clients the new client has joined
            self.broadcast(f'{username} has joined the server!\n'.encode('ascii'))

            # Sends a message to the client saying they have connected
            client.send('You have successfully connected to the server\n'.encode('ascii'))

            # Thread made for new client
            thread = threading.Thread(target=self.handle, args=(client,))

            # Start runnning Thread
            thread.start()

    def run(self):
        print('Host IP: ', self.host)
        print('Server v3 is now active\n')
        self.receive()

# Run server
if __name__ == "__main__":
    server = Server()
    server.run()