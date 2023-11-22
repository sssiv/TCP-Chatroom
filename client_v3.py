import socket
import threading

# Client class
class Client:
    # Get host IP, port, username
    def __init__(self, host, port, username):
        # Client Socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect Client
        self.client.connect((host, port))

        # Client username
        self.username = username

        # Remain connected flag
        self.connected = True

    # Recieve messages
    def receive(self):
        while self.connected:
            # Send a message
            try:
                # If the secieved message is to obtain the username
                message = self.client.recv(1024).decode('ascii')
                if message == 'Enter a username: ':
                    self.client.send(self.username.encode('ascii'))
                
                # Else its a message from another user in the server
                else:
                    print(message)

            # Error recieving message
            except Exception as e:
                print(f'An error occurred: {e}\n')
                break

    # Write message to send
    def write(self):
        while self.connected:
            # Write a message
            try:
                # The message contains your username in it
                message = f'{self.username}: {input("")}'

                # Disconenct command
                if message.endswith('!LEAVE'):
                    self.client.send('!LEAVE'.encode('ascii'))
                    self.connected = False

                # If the D/C command isnt used, send your message to the server
                else:
                    self.client.send(message.encode('ascii'))
            
            # Error writing and sending message
            except Exception as e:
                print(f'An error occurred: {e}\n')
                self.connected = False
                break

if __name__ == "__main__":
    port = 12345
    network_part = '192.168.1.'
    host_part = input('Enter in host part: ')
    host = network_part + host_part
    username = input('Enter a username: ')
    client = Client(host, port, username)

    with client.client:
        receive_thread = threading.Thread(target=client.receive)
        write_thread = threading.Thread(target=client.write)

        receive_thread.start()
        write_thread.start()

        receive_thread.join()
        write_thread.join()
