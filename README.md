# test_kanalservice
Тестовое на Python разработчика

ТЗ:
Необходимо разработать скрипт на языке Python 3, 

который будет выполнять следующие функции:

1. Получать данные с документа при помощи Google API, сделанного в [Google Sheets](https://docs.google.com/spreadsheets/d/1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g/edit) (необходимо копировать в свой Google аккаунт и выдать самому себе права).
2. Данные должны добавляться в БД, в том же виде, что и в файле –источнике, с добавлением колонки «стоимость в руб.»
    
    a. Необходимо создать DB самостоятельно, СУБД на основе PostgreSQL.
    
    b. Данные для перевода $ в рубли необходимо получать по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).
    
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (необходимо учитывать, что строки в Google Sheets таблицу могут удаляться, добавляться и изменяться).

4. a. Упаковка решения в docker контейнер
    
    b. Разработка функционала проверки соблюдения «срока поставки» из таблицы. В случае, если срок прошел, скрипт отправляет уведомление в Telegram.
    
    c. Разработка одностраничного web-приложения на основе Django или Flask. Front-end React.


### Инструкция по запуску:  
docker-compose up --build

если вдруг выйдет вот такая ошибка:  
![Screenshot_20220727_215425](https://user-images.githubusercontent.com/38224171/181366260-f866ed47-3dfa-41de-a097-800dd00b4fc2.png)  
то остановите докер ctrl + c и запустите его заново docker-compose up --build  
   
сайт распологается по адресу 127.0.0.1 (Запускал докер на виндовс)
[таблица эксель](https://docs.google.com/spreadsheets/d/1IxOrx-AWiK0Xz-gi9K_ex8NyzW1To4MwV7AyBCbVVzU/edit#gid=0)  



# PS

вам нужны свои креды от гугл апи с доступом к гугл щитс и гугл диску
