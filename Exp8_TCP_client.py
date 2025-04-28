import socket

def receive_file(filename='received_file.txt', host='localhost', port=12345):
        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    with open(filename, 'wb') as file:
        print(f"Receiving {filename}...")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
        print(f"File {filename} received successfully.")
    

    client_socket.close()

receive_file('rcvd_helloworld.txt') #Pass ip parameter if recieving from another machine
