import socket
import argparse
import threading
import time
import cx_Oracle

# DB 접속
conn = cx_Oracle.connect("miniproject", "miniproject", "localhost:1521/xe")
cur = conn.cursor()

host = ""
port = 4000
user_list = {}
notice_flag = 0

def data_base_admin(admin_socket, admin): # 관리자가 dB에 접근해서 작업할 때의 함수
    while True:
        data = client_socket.recv(8192)
        db_query = data.decode() # db_query = select * from player
        db_query_repr = "%s : %s" % (user, db_query)
        print(db_query_repr)

        if db_query == "/exit":
             break
        cur.execute(db_query)
        query_result = cur.fetchall()

        try:
            for tuple in query_result:
                print(tuple)
                admin_socket.send(str(tuple).encode())
                time.sleep(0.05)
            print("이제 쿼리 결과가 끝났어")
            admin_socket.send("이제 쿼리 결과가 끝났어".encode())
        except:
            print("abnormal")
    del user_list[user]
    client_socket.close()

def handle_notice(client_socket, addr, user): # 사용자들이 게임에 접속 해서 포커를 치는 함수
    pass


print("Setting server...")
#IPv4 체계, TCP 타입 소켓 객체를 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#포트를 사용 중 일때 에러를 해결하기 위한 구문
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#ip주소와 port번호를 함께 socket에 바인드 한다.
server_socket.bind((host, port))

#서버가 최대 5개의 클라이언트의 접속을 허용한다.
server_socket.listen(5)
print("Setting server - 5 clients")

while 1:
    try:
        #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
        client_socket, addr = server_socket.accept()
    except KeyboardInterrupt:
        for user, con in user_list:
            con.close()
        server_socket.close()
        print("Keyboard interrupt")
        break
    user = client_socket.recv(1024).decode()
    user_list[user] = client_socket

    #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
    notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr, user))
    notice_thread.daemon = True
    notice_thread.start()


    receive_thread = threading.Thread(target=data_base_admin, args=(client_socket, user))
    receive_thread.daemon = True
    receive_thread.start()