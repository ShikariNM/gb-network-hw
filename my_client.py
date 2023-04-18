import socket
import threading

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occured!')
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('ascii'))

nickname = input("\nChoose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 1379))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

recieve_thread = threading.Thread(target=write)
recieve_thread.start()