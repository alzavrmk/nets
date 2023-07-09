import socket
import threading# многопоточность

# Choosing Nickname Выбор псевдонима
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
# рождается сокет

# Listening to Server and Sending Nickname Прослушивание сервера и отправка псевдонима
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
# Запуск Потоков для Прослушивания И Записи
receive_thread = threading.Thread(target=receive)
receive_thread.start()
# tread позволяет организовать многопотчность, те одновременную работу
# двух бесконечных циклов в данном случае
write_thread = threading.Thread(target=write)
write_thread.start()

