import socket
import _thread as thread
import time


def receive_messages(recieve_socket):
    while True:
        print (recieve_socket.recv(1024))


def send_messages(send_socket):
    while True:
        data = input()
        send_socket.send(data.encode())    

def main():
    my_socket = socket.socket()
    my_socket.connect(('220.67.124.117', 8823))

    thread.start_new_thread(send_messages, (my_socket, ))
    thread.start_new_thread(receive_messages, (my_socket, ))
    time.sleep(1)  #this delay lets the threads kick in, otherwise the thread count is zero and it crashes
    while thread._count() > 1:
        thread.start_new_thread(send_messages, (my_socket, ))
        thread.start_new_thread(receive_messages, (my_socket, ))

if __name__ == '__main__':
    main()