# Шардирование

1. Используется [docker-compose.yml](docker-compose.yml), для запуска citus

2. Запускаем citus, подключаемся к master и создаем таблицу для хранения диалогов:

```
CREATE TABLE dialogs (
    id bpchar NOT NULL,
    partion_id bigint NOT NULL,
    from_user_id bpchar NOT NULL,
    to_user_id bpchar NOT NULL,
    text bpchar,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (partion_id, id)
);
```
   Шардирование будет осуществляться по полю partion_id, который будет заполняться образом (сумма хэшей от id пользователей) чтобы он совпадал для диалогов двух пользователй неважно кто из них отправитель и кто получатель. Таким образом диалоги, когда пользователь 1 - отправитель, а пользователь 2 - получатель, всегда будут находится в одной партиции с диалогами, когда пользователь 1 - получатель, а пользователь 2 - отправитель. 


3. Делаем ее распределенной
```
SELECT create_distributed_table('dialogs', 'partion_id');
```

4. Чтобы сохранить диалог между пользователями необходимо вызвать метод `POST /api/v1/dialog/<user_id>/send`

5. Чтобы получить переписку между двумя пользователями необходимо вызвать метод `GET /api/v1/dialog/<user_id>/list`
