#!/bin/python3
import socket
import threading

# Connection Data
host = 'localhost'
port = 1379

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
# Заменил списки на словарь
chat_participants = {}

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in chat_participants:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            decoded_message = message.decode('ascii')
            # Если в сообщение есть $, значит оно личное
            if '$' in decoded_message:
                # Из сообщения вида "отправитель: получатель$текст сообщения"
                # нужно извлечь текст сообщения и получателя
                actual_message = decoded_message.split('$')[1]
                nickname = decoded_message.split('$')[0].split(' ')[1]
                # Если у сервера есть контакт с получателем, отправляет сообщение ему.
                # Если нет, информирует отправителя
                if nickname in chat_participants.values():
                    recipient = get_key(chat_participants, nickname)
                    recipient.send(
                        f'from {chat_participants[client]}: {actual_message}'.encode('ascii')
                        )
                else:
                    client.send(f'{nickname} is out of chat'.encode('ascii'))
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            client_to_remove = chat_participants[client]
            chat_participants.pop(client, None)
            client.close()
            print(f'{client_to_remove} has left')
            broadcast(f'{client_to_remove} left!'.encode('ascii'))
            break

def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        chat_participants[client] = nickname

        # Print And Broadcast Nickname
        print(f"Nickname is {nickname}")
        client.send('''\nConnected to server!
        \rIf you want to send an individual message,
        \radd "nickname$" at the beginning of the message.\n'''.encode('ascii'))
        broadcast(f"{nickname} joined!".encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()
