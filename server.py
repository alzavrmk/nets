#!/bin/python3
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET - ipv4 адрес, socket.SOCK_STREAM - TCP
server.bind((host, port))
server.listen()  # переводим сервер в слушающее состояние

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients Отправка Сообщений Всем Подключенным Клиентам
def broadcast(message):
    for client in clients:
        client.send(message)
        # send - писать или послать


# Handling Messages From Clients Обработка сообщений от Клиентов
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            # recv читать
            # message = client.recv(1024) принять сообщение с буфером 1024
            broadcast(message)  # отправить всем
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)  # удаляем клиента
            client.close()  # закрываем его чат
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            # выводим сообщение
            nicknames.remove(nickname)
            # удаляем никнейм
            break


# Receiving / Listening Function # Функция приема / прослушивания
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        #
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname запросить и Сохранить Псевдоним
        client.send('NICK'.encode('utf-8'))
        #
        nickname = client.recv(1024).decode('utf-8')
        # принимаем никнейм  клиента
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname Печатный и Широковещательный псевдоним
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server if listening...")
receive()
