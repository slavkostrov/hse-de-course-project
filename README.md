# Проект по курсу DE

### Инструкция по запуску

1. Создать окружение с Python 3.12.
2. Установить poetry с помощью `pip install poetry`.
3. Установить зависимости с помощью `poetry install`.
4. Выставить переменную окружения AIRFLOW_HOME в корень репозитория.
5. Создать `.env` файл с заполнением следующих полей:
    ```
    HOST=""
    PORT=
    DATABASE=""
    USER=""
    PASSWORD=""```
6. Создать конфиг Airflow и выполнить `airflow config list --defaults > "${AIRFLOW_HOME}/airflow.cfg"`, настроить необходимые параметры (например, выключить загрузку примеров).
7. Запустить Airflow (для примера в standalone режиме) с помощью `TABLE_PREFIX="<your_prefix>" airflow standalone`, где TABLE_PREFIX - префикс для имени все создаваемых таблиц.
8. Даг будет запускать ежедневно по расписанию, либо можно запустить даг передав в json конфигурацию рана конкретную дату (date), за которую хочется собрать отчет.


### Описание пайплайна

1. Таблицы читаются из источников (из базы или из файла), затем они валидируются с помощью Pydantic моделей так, что "плохие" записи не попадут в базу сразу, проверенные записи загружаются в стейджинг версию таблицы.
2. Из стейджинг таблицы данные перекладываются в DIM таблицу, добавляя или изменяя колонки `create_dt` и `update_dt`, таким образом в DIM таблице хранися только последняя версия данных и информация о том, когда она была создана или изменена (SCD1).
3. Из DIM таблицы данные перекладываются в DIM_HIST таблицу (SCD2) с добавлением соотв. полей.
4. Таблицы с фактами перекладываются в целевые таблицы из стейджинга без дополнительных изменений.
5. Строится отчет о фроде.
6. Делается бэкап файлов-источников.

Взаимодействие с базой реализовано с помощью sqlalchemy (что возможно местами получилось не очень эффективно из-за выгрузки в память, но захотелось в этом покопаться, переписать на select from insert вроде не проблема), валидация данных с помощью Pydantic, расписание с помощью Airflow.


Вид дага:

<img width="1713" alt="image" src="https://github.com/user-attachments/assets/3443a5db-37d4-4ab7-bd1e-4c65388eae26" />
