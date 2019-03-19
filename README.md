# task-3

Клиент серверное приложение на сокетах, реализующее игру в крестики/нолики для двух человек по сети.
Для передачи данных используется модуль стандартной библиотеки socket.
Программа предоставляет текстовый интерфейс для ввода ходов и отображения игрового поля. Далее игроки на сервере и клиенте начинают делать ходы по очереди, пока один из них не победит.

## Examples:
Запуск сервера:
```bash
make start_server
```

Запуск клиента:
```bash
make start_client
```

Сделать ход:
```bash
Ваш ход: A 3
```

### Create virtualenv and install requirements

    make init

### Run autoformat

    make pretty

### Run linters

    make lint

### Run tests

    make test

### Add precommit hook

    make precommit_install
