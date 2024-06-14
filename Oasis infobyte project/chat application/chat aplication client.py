import socket
import threading

nickname = input("Enter your nickname: ")
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NICK':
                client_socket.send(input('Enter your nickname: ').encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def main():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        message = f'{nickname}: {input("")}'.encode('ascii')
        client_socket.send(message)

if __name__ == "__main__":
         main()