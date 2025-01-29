import socket

def main():
    host = 'localhost'
    port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
    except KeyboardInterrupt:
        print("Client disconnected")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()