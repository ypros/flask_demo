# Онлайн обновление ленты новостей

1. Был изменен метод `api/v1/post/create` - вместо сохранения поста в базу, он записывается в очередь rabbitmq
2. Был добавлен подополнительный сервис, который слушает очередь и при получении нового сообщения сохраняет его в БД.
   Для запуска дополнительного сервиса `python rabbitmq/listener.py`

3. Для обмена сообщениями был поднят rabbitmq и добавлена очередь`flask-queue`
