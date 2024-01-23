# Restaurant API
## Описание
---
Простой REST-сервис, реализует меню

---
## Запуск для тестирования
- У вас должен быть установлен докер, запустите его
- Активируйте виртуальное окружение
- Установите зависимости
- Выполните
  - ```docker run --name restaurantapi -p 127.0.0.1:5433:5432 -e POSTGRES_USER=test_user -e POSTGRES_PASSWORD=test_pass -e     POSTGRES_DB=resapi -d postgres```
- Выполните
  - ```alembic revision --autogenerate -m "firstmigration"```
  - ```alembic upgrade head```
  - ```python main.py```
- Проект готов к тестированию


---
## Автор: Semyonov-K
