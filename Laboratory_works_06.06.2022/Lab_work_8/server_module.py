import socket


def server_module(port: int) -> None:
    """ Серверный модуль:
        1. Создаёт сокет.
        2. Связывается с хостом и портом.
        3. Запускает режим прослушивания порта с максимальным количеством подключений в очереди - 1.
        4. Принимает подключение адрес и сокет клиента.
        5. Далее - поддерживает диалог отправляя сообщения клиента обратно в верхнем регистре до того момента
           пока пользователь не отправит сообщение 'до свидания', затем закрывает соединение.
        6. Принимает данные порциями по 1024 байт = 1кб."""

    host = socket.gethostname()
    sock = socket.socket()  # *1
    sock.bind((host, port))  # *2
    sock.listen(1)  # *3
    connect, address = sock.accept()  # *4

    while True:  # *5
        data = connect.recv(1024)  # *6
        if not data:
            break

        data = data.decode()

        if data.lower().strip() == "до свидания":
            connect.send(('До свидания!'.encode()))
            connect.close()
            break

        connect.send(('Я эхо бот - ' + data.upper()).encode())


if __name__ == '__main__':

    server_module(5555)
