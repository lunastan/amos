import socket
import threading

# 접속하고 싶은 ip와 port를 입력받는 클라이언트 코드를 작성해보자. 
# 접속하고 싶은 포트를 입력한다. 
port = 4000
host = '192.168.0.7'

print("Setting chatting client...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

#user = input("Enter user name:")
user = 'admin'
client_socket.sendall(user.encode())
print("Setting client complete...")
print("Welcome ", user)

while True:
    message = input("Enter SQL Query: ")
    if message == "/exit":
        break
    client_socket.send(message.encode())
    while True:
        data = client_socket.recv(1024).decode()
        if data == "이제 쿼리 결과가 끝났어":
            # print(data)
            break;
        print(data)


client_socket.close()

# def handle_receive(num, client_socket, user):
#     while 1:
#         try:
#             data = client_socket.recv(8192)
#         except:
#             print("연결 끊김")
#             break
#         data = data.decode()
#         # if not user in data:
#         print(data)
# def handle_send(num, client_socket):
#     while 1:
#         query = input("Enter SQL Query: ")
#         data = query.encode()
#         client_socket.sendall(data)
#         if data == "/exit":
#             break
#client_socket.close()


# receive_thread = threading.Thread(target=handle_receive, args=(1, client_socket, user))
# receive_thread.daemon = True
# receive_thread.start()
#
# send_thread = threading.Thread(target=handle_send, args=(2, client_socket))
# send_thread.daemon = True
# send_thread.start()
#
# send_thread.join()
# receive_thread.join()