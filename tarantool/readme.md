# Tarantool как хранилище диалогов

## Установка и настройка tarantool

1. Установка и запуск Tarantool в докере: 
   ``` 
   docker run \
   --name tarantool \
   -d -p 3302:3302 \
   -v $PWD/volumes/tarantool:/var/lib/tarantool \
   tarantool/tarantool
   ```

2. Настройка space для хранения диалогов - dialogs.
   ``` lua
   box.once('init', function()
	dialogs = box.schema.create_space('dialogs', { if_not_exists = true })
	dialogs:format({{ name = 'dialog_id', type = 'uuid', is_nullable = false}, { name = 'user_from_id', type = 'uuid', is_nullable = false}, { name = 'user_to_id', type = 'uuid', is_nullable = false}, { name = 'text', type = 'string', is_nullable = false}, { name = 'created_at', type = 'datetime', is_nullable = false}})

	dialogs:create_index('pk', { parts = { { field = 'dialog_id', type = 'uuid'}}})
	dialogs:create_index('user_from_k', { parts = { { field = 'user_from_id', type = 'uuid'}}, unique = false})
	dialogs:create_index('user_to_k', { parts = { { field = 'user_to_id', type = 'uuid'}}, unique = false})
   end)
   ```

3. Добавление функций для записи и чтения диалогов пользователей:
   ``` lua
   lua_code = [[function(dialog_id, user_from, user_to, text)
   uuid = require('uuid')
   datetime = require('datetime')
   new_uuid = uuid.new()
   box.space.dialogs:insert{new_uuid, dialog_id, uuid.fromstr(user_from), uuid.fromstr(user_to), text, datetime.now()}
   return new_uuid:str() end]]

   box.schema.func.create('new_dialog', {body = lua_code})
   lua_code = [[function(dialog_id)
   return box.space.dialogs.index.dialog_id_k:select({dialog_id})
   end]]

   box.schema.func.create('get_dialog', {body = lua_code})
   ```

4. Доступ пользователю, под которым будет подключать наше приложение, к спейсу и фукнциям
   ``` lua
   box.schema.user.grant('guest', 'execute', 'function', 'new_dialog')
   box.schema.user.grant('guest', 'execute', 'function', 'get_dialog')
   box.schema.user.grant('guest', 'read,write,execute', 'universe')
   ```

## Тестирование производительности

  Для запросов к tarantool использовалась библиотека `tarantool/tarantool-python`
  Из приложения вызывались встроенные функции на lua.

### Запись нового диалога двух пользователей

   Запись в posgres

   ![post dialog users 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/post%20dialog%20users%2010.png)
   ![post dialog users 50.png](https://github.com/ypros/flask_demo/blob/main/tarantool/post%20dialog%20users%2050.png)

   Запись в tarantool

   ![post dialog tarantool 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/post%20dialog%20tarantool%2010.png)

### Выборка всех диалогов между пользователями

   Чтение из postgres

   ![read dialog 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/read%20dialog%2010.png)
   ![read dialog stats 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/read%20dialog%20stats%2010.png)

   Чтение из tarantool

   ![read dialog tarantool 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/read%20dialog%20tarantool%2010.png)
   ![read dialog tarantool stats 10.png](https://github.com/ypros/flask_demo/blob/main/tarantool/read%20dialog%20tarantool%20stats.png)

### Вывод

   Чтение и запись в tarantool выполняется быстрее при нагрузке в 10 потоков. При увеличении нагрузки до 50 потоков, сервис выдавал ошибки при чтении и записи в tarantool, в отличие от posgres. Вероятно для подключения к tarantool лучше использовать другую библиотеку позволяющую делать запросы асинхронно. Сравнение библиотек https://www.tarantool.io/en/doc/latest/book/connectors/python/

