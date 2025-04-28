import socket

def send_file(filename, host='localhost', port=12345):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
        

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")


    with open(filename, 'rb') as file:
        print(f"Sending {filename}...")
        data = file.read()
        conn.sendall(data)
    print(f"File {filename} sent successfully.")
    
    conn.close()
    server_socket.close()


send_file('helloworld.txt') #Pass bind ip parameter if sending to another machine '0.0.0.0' for all interfaces or enter interface ip
