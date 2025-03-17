1) Поднимаем приложение и postgresSQL    

        docker compose --env-file .template.env.docker up -d

2) Заходим в контейнер приложения 

        docker exec -it app /bin/bash

3) Делам миграции 

        alembic --config app/alembic.ini upgrade head

4) Загружаем фикстуры 

        python app/commands/data_filter.py

5) Запускаем обработку 1-го документа, согласно заданию

        python app/main.py


