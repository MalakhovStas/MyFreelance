import socket
import time


def client_module(port: int) -> None:
    """ Клиентский модуль:
        1. Создаёт сокет.
        2. Подключается к серверу.
        3. Поддерживает диалог, до того момента пока пользователь не отправит сообщение 'до свидания',
           затем закрывает соединение.
        4. Принимает данные порциями по 1024 байт = 1кб."""

    host = socket.gethostname()
    sock = socket.socket()  # *1
    sock.connect((host, port))  # *2

    while True:  # *3
        message = input('Введите сообщение: ')
        sock.send(message.encode())
        data = sock.recv(1024)  # *4
        if data:
            data = data.decode()
            print(f'Ответ сервера: {data}\n')
        if data == 'До свидания!':
            sock.close()
            time.sleep(30)
            break


if __name__ == '__main__':

    client_module(5555)
