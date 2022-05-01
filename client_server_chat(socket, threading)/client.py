import socket
import threading


# Слушаем сообщения от сервера
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Error: client are connected':
                error_message = message
                raise Exception('Client are joined')
            elif message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Закрываем соединение при ошибке
            print(f"An error occured! {error_message}")
            client.close()
            print('Сlose connect...')
            break
            # может через рейз дропать?
            # raise Exception('Client are joined')


# Отправка сообщения на сервер
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


if __name__ == '__main__':
    # Выбор Никнейма
    nickname = input("Choose your nickname: ")

    # Создание серверного соединения
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 2022))

    # Запуск потоков для прослушивания сообщений от сервера и отправки сообщений на сервер
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()
