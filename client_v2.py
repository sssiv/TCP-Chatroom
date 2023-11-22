# Difference from V1:
#   * uses pythons "with" context manager

import socket
import threading

# Get message from other clients
def recieve(client):
    global connected
    # while remaining connection
    while connected:
        # Try recieving a message
        try:
            # Prompt from if the message is asking for a username
            message = client.recv(1024).decode('ascii')
            if message == 'Enter a username: ':
                client.send(username.encode('ascii'))

            # Else the message is from a user
            else:
                print(message)
        # There was an error recieving messages
        except Exception as e:
            print(f'An error occurred: {e}\n')
            break

# Write and send message to server to send to clients
def write(client):
    # while remaining connection
    global connected
    while connected:
        # Try writing and sending a message
        try:
            # Message input
            message = f'{username}: {input("")}'

            # The leave server command 
            if message.endswith('!LEAVE'):
                client.send('!LEAVE'.encode('ascii'))
                connected = False

            # Else you stay in the server and send your message
            else:
                client.send(message.encode('ascii'))

        # Error creating and sending your message
        except Exception as e:
            print(f'An error occurred: {e}\n')
            connected = False
            break

if __name__ == "__main__":
    # Listening Port
    port = 12345

    # Subnet
    network_part = '192.168.1.'

    # enter host part of IP
    host_part = input('Enter in host part: ')

    # Subnet + IP
    host = network_part + host_part

    # Client username
    username = input('Enter a username: ')

    # While we are using the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Connect client with the IP and listening port
        client.connect((host, port))

        # Connection flag for the functions
        connected = True

        # When accessing local variables, you need to use args=
        receive_thread = threading.Thread(target=recieve, args=(client,))
        write_thread = threading.Thread(target=write, args=(client,))

        # Start threads
        receive_thread.start()
        write_thread.start()

        # Makes sure each thread finishes before closing
        receive_thread.join()
        write_thread.join()