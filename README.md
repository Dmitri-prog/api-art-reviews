## Проект API сайта отзывов на художественные произведения
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)


### Описание проекта.

API cайта отзывов пользователей на художественные произведения (музыка, книги, фильмы и т.д.), с возможностью оценки произведений и автоматического формирования рейтинга произведения на их основе. Также осуществлена возможность комментирования чужих отзывов.

В проекте реализована авторизация и аутентификация пользователей по JWT-токенам с подтверждением регистрации через e-mail.

Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Dmitri-prog/api-art-reviews
```

```
cd api_reviews
```

2. Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
```
```
source venv/bin/activate
```

3. Обновить PIP

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

4. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

5. Перейти в директорию с файлом manage.py и выполнить миграции:

Windows
```
cd api_reviews
```
```
python manage.py migrate
```

Linux/macOS
```
cd api_reviews
```
```
python3 manage.py migrate
```

6. Запустить проект:

Windows
```
python manage.py runserver
```

Linux/macOS
```
python3 manage.py runserver
```

### Некоторые примеры запросов к API.

Доступные энд-поинты: GET-запросы списков

```
http://127.0.0.1:8000/api/v1/categories/
```
```
http://127.0.0.1:8000/api/v1/genres/
```
```
http://127.0.0.1:8000/api/v1/titles/
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
http://127.0.0.1:8000/api/v1/users/
```

Все доступные варианты запросов к API, а также примеры ответов API можно посмотреть после запуска проекта в его документации, выполнив запрос
```
http://127.0.0.1:8000/redoc/
```

#### Авторы
Родион Смирнов
Борис Ашанин
Марков Дмитрий