# Нагрузочный тест - Производительность индексов
## Цель теста
Проверить работу сервиса под нагрузкой.
Определить наиболее подходящий индекс для поиска пользователей

## Подготовка к тесту
1. Было создано 1 000 000 записей в таблицу users
2. Для тестирования был выбран запрос поиска пользователей по имени и фамили:
`"SELECT id, first_name, last_name, age, biography, city FROM users WHERE first_name LIKE %s AND last_name LIKE %s ORDER BY id"`
3. Для тестиования были отобраны топ 30 по количеству фамилий (первые 3 буквы) и топ 20 имен (первые 2 буквы)
4. Для тестов использовался JMeter

## Тестирование
### Без индекса 
| Label | # Samples | Average | Min | Max | Std. Dev. | Error % | Throughput | Received KB/sec | Sent KB/sec | Avg. Bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 user | 20 | 402 | 372 | 507 | 28.58 | 0.000% | 2.47249 | 353.19 | 0.46 | 146275.8 |
| 10 users | 522 | 870 | 392 | 1632 | 224.75 | 0.000% | 8.57932 | 731.52 | 1.59 | 87311.3 |
| 100 users | 579 | 8477 | 447 | 14391 | 3495.02 | 0.000% | 8.74966 | 741.81 | 1.62 | 86816.2 |
| 1000 users | 169 | 4358 | 1 | 8407 | 2122.41 | 89.349% | 17.46770 | 328.56 | 0.40 | 19260.9 |

Тест на 1000 не был выполнен до конца, при количестве потоков > 148 сервис стал отдавать 500 ошибку

### 2 индекса на first_name (btree) и last_name (btree)
| Label | # Samples | Average | Min | Max | Std. Dev. | Error % | Throughput | Received KB/sec | Sent KB/sec | Avg. Bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 user | 20 | 75 | 42 | 282 | 41.16 | 0.000% | 16.84492 | 2173.13 | 3.19 | 146275.8 |
| 10 users | 1850 | 242 | 30 | 1736 | 192.25 | 0.000% | 30.82100 | 2579.19 | 5.72 | 85691.4 |
| 100 users | 2157 | 2135 | 67 | 7023 | 1007.05 | 0.000% | 34.66341 | 2905.07 | 6.43 | 85819.4 |
| 1000 users | 483 | 1843 | 0 | 5341 | 1045.38 | 36.025% | 48.55735 | 2584.80 | 5.76 | 54509.5 |

Тест на 1000 не был выполнен до конца, при количестве потоков > 170 сервис стал отдавать 500 ошибку

### 1 индекс на first_name и last_name (btree)
| Label | # Samples | Average | Min | Max | Std. Dev. | Error % | Throughput | Received KB/sec | Sent KB/sec | Avg. Bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 user | 20 | 55 | 31 | 210 | 38.91 | 0.000% | 17.87310 | 2553.13 | 3.32 | 146275.8 |
| 10 users | 1192 | 188 | 29 | 1462 | 133.42 | 0.000% | 39.74128 | 3317.34 | 7.37 | 85476.9 |
| 100 users | 2493 | 1861 | 51 | 7603 | 951.76 | 0.000% | 39.99615 | 3343.96 | 7.42 | 85613.6 |
| 1000 users | 501 | 1520 | 0 | 5224 | 874.03 | 32.934% | 54.89809 | 2965.00 | 6.83 | 55305.4 |

Тест на 1000 не был выполнен до конца, при количестве потоков > 160 сервис стал отдавать 500 ошибку

### Сранение показателей для тест на 100 пользователей
#### active threads
![active threads 100 ind 1](https://user-images.githubusercontent.com/9604702/215865968-cbd21da0-b1b5-441c-a3d7-6fc7e99e0426.png)
#### Latencies
![Latencies 100](https://user-images.githubusercontent.com/9604702/215866106-e729ef48-6b6e-4047-aa45-d038ff63e036.png)
![Latencies 100 ind 1](https://user-images.githubusercontent.com/9604702/215866134-597d12f5-9124-4814-a572-6b4e0a0aa6eb.png)
![Latencies 100 ind 2](https://user-images.githubusercontent.com/9604702/215866149-6579d3a6-7f21-44bc-8202-a053d5621de6.png)
#### Throughput
![Throughput 100](https://user-images.githubusercontent.com/9604702/215866357-14938f29-1ac8-4278-8e00-bbc80f074043.png)
![Throughput 100 ind 1](https://user-images.githubusercontent.com/9604702/215866381-58fec95e-f040-45a6-b76a-b64532c77314.png)
![Throughput 100 ind 2](https://user-images.githubusercontent.com/9604702/215866387-0651e614-176e-4593-bfc0-eaccad99f38c.png)

### Запрос на создание индекс
1. `CREATE INDEX users_first_name_IDX USING BTREE ON flask.users (first_name);
  CREATE INDEX users_last_name_IDX USING BTREE ON flask.users (last_name);`
2. `CREATE INDEX users_first_name_IDX USING BTREE ON flask.users (first_name,last_name);`

### explain запроса
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SIMPLE | u |  | range | users_first_name_IDX | users_first_name_IDX | 404 |  | 122786 | 11.11 | Using index condition; Using MRR |

## Вывод
Тесты показали что наиболее эффективным индексом для данного запроса являет двойной индекс по полям first_name, last_name
