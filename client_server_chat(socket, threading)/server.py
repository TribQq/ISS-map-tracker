import socket
import threading


# Данные соединения
host = '127.0.0.1'
port = 2022

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Список клентов и их никнеймы
clients = []
nicknames = []


# Отправка сообщения клиентам
def broadcast(message):
    for client in clients:
        client.send(message)


# Обработка действий клиента
def handle(client):
    while True:
        try:
            # Широковещательное сообщение
            message = client.recv(1024)
            broadcast(message)
        except:
            # Удаление клиента и закрытие соединения
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Принятие соединения
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        # Запрос и созданение никнейма
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        print("Nickname is {}".format(nickname))

        # автоматический ренейм вместо рейза
        # if nickname in nicknames:
        #     nickname = nickname + str(nicknames.count(nickname) + 1)

        if nickname not in nicknames:
            nicknames.append(nickname)
            clients.append(client)
            # Сообщение о присоединении клиента
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            # Запуск и обработка потока для клиента
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
            print(clients)
            print(nicknames)
        else:
            client.send('Error: client are connected'.encode('ascii'))


if __name__ == '__main__':
    print('Start server')
    receive()
    print('end server')
