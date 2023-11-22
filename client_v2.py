import socket
import threading

def recieve(client):
    global connected
    while connected:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Enter a username: ':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f'An error occurred: {e}\n')
            break

def write(client):
    global connected
    while connected:
        try:
            message = f'{username}: {input("")}'
            if message.endswith('!LEAVE'):
                client.send('!LEAVE'.encode('ascii'))
                connected = False
            else:
                client.send(message.encode('ascii'))
                
        except Exception as e:
            print(f'An error occurred: {e}\n')
            connected = False
            break

if __name__ == "__main__":
    port = 12345
    network_part = '192.168.1.'
    host_part = input('Enter in host part: ')
    host = network_part + host_part
    username = input('Enter a username: ')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        connected = True

        # When accessing local variables, you need to use args=
        receive_thread = threading.Thread(target=recieve, args=(client,))
        write_thread = threading.Thread(target=write, args=(client,))

        receive_thread.start()
        write_thread.start()

        receive_thread.join()
        write_thread.join()
