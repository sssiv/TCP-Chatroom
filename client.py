import threading
import socket

# If host is acting up, set host in server and here to 127.0.0.1

# Port isn't reserved so I chose it
port = 12345        

# takes in an IP address and Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server IP
network_part = '192.168.1.'
host_part = input('Enter in server IP: ')
host = network_part + host_part

# Creates an input string to get username from client
username = input('Pick a username: ')

# Connect the client to the server
client.connect((host, port))

# Flag to see if connection gets terminated
connected = True

# Recieve clients messages from the server
def recieve():
    global connected
    while connected:
        # Try executing code in this block
        try: 
            # Attempt to recieve messages from clients 
            # Decode to bytes
            message = client.recv(1024).decode('ascii')

            # When the server prompts to enter a username,
            # that username is sent to the server
            if message == 'Enter a username: ':
                client.send(username.encode('ascii'))
                pass

            # When you enter in a prompt,
            # The server is no longer sending messages to the client directly
            # therefore, the message should be anything else
            # But what happens when the users message is 'Enter a username: '?
            else:
                print(message)

        # If an exception/error occurs in the try block, do this
        except:
            print('An error occured!\n')
            client.close()
            break

# Writes message to send from client to server to the rest of the chat
def write():
    global connected
    while connected:
        try:
            # The message sent from the client
            # Will be outputted as "Username: whatever message they wrote"
            message = f'{username}: {input("")}'

            # Looks for specific message to disconnect
            if message.endswith('!LEAVE'):
                # Send the leave command to the server
                client.send(f'{username}!LEAVE'.encode('ascii'))  
                connected = False
            else:
                # Sends message from client
                client.send(message.encode('ascii'))

        # catches exception/error as variable e
        except Exception as e:
            # Displays exception/error
            print(f'An error occurred: {e}\n')
            connected = False

            # Try to close client connection
            try:
                client.close()
            # If that fails, exception/error as variable e
            except Exception as e:
                # Display errpr/exception
                print(f'Failed to close the connection: {e}\n')
            break  # Exit the write loop

# Creates a thread to reviece messages between users
recieve_thread =  threading.Thread(target=recieve)

# Activates recieving thread
recieve_thread.start()

# Creates a thread to write messages between users
write_thread =  threading.Thread(target=write)

# Activates writing thread
write_thread.start()