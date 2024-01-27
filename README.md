## Стек используемых технологий:
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


### Автор проекта: [Михаил Медведев](github.com/mikhail-medvedev90 "Author's github")

# Foodgram - это ваш цифровой кулинарный помощник.
__FOODGRAM - "продуктовый помощник".__  
_Он создан для начинающих кулинаров и опытных гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать в формате .txt сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд._  


## Как запустить проект?

Программа поднимается на порту 8500.

PostgreSQL поднимается на порту 5432.


1. Скачиваем проект:  
```
git clone git@github.com:mikhail-medvedev90/foodgram-project-react.git
```
2. Далее в корне проекта создадим файл .env и добавляем в него данные в формате, указанном в файле `.env.example`:

3. Переходим в папку `/infra`, где мы "поднимаем" приложение, собираем статику, запускаем миграции и создаем суперюзера:
```
cd infra/
sudo docker compose up
sudo docker compose exec backend python manage.py collectstatic
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
```

## API проекта

`/api/users/` Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя. Доступно без токена.

`/api/users/{id}` GET-запрос – персональная страница пользователя с указанным id (доступно без токена).

`/api/users/me/` GET-запрос – страница текущего пользователя. PATCH-запрос – редактирование собственной страницы. Доступно авторизированным пользователям.

`/api/users/set_password` POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям.

`/api/auth/token/login/` POST-запрос – получение токена. Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.

`/api/auth/token/logout/` POST-запрос – удаление токена.

`/api/tags/` GET-запрос — получение списка всех тегов. Доступно без токена.

`/api/tags/{id}` GET-запрос — получение информации о теге о его id. Доступно без токена.

`/api/ingredients/` GET-запрос – получение списка всех ингредиентов. Подключён поиск по частичному вхождению в начале названия ингредиента. Доступно без токена.

`/api/ingredients/{id}/` GET-запрос — получение информации об ингредиенте по его id. Доступно без токена.

`/api/recipes/` GET-запрос – получение списка всех рецептов. Возможен поиск рецептов по тегам и по id автора (доступно без токена). POST-запрос – добавление нового рецепта (доступно для авторизированных пользователей).

`/api/recipes/?is_favorited=1` GET-запрос – получение списка всех рецептов, добавленных в избранное. Доступно для авторизированных пользователей.

`/api/recipes/is_in_shopping_cart=1` GET-запрос – получение списка всех рецептов, добавленных в список покупок. Доступно для авторизированных пользователей.

`/api/recipes/{id}/` GET-запрос – получение информации о рецепте по его id (доступно без токена). PATCH-запрос – изменение собственного рецепта (доступно для автора рецепта). DELETE-запрос – удаление собственного рецепта (доступно для автора рецепта).

`/api/recipes/{id}/favorite/` POST-запрос – добавление нового рецепта в избранное. DELETE-запрос – удаление рецепта из избранного. Доступно для авторизированных пользователей.

`/api/recipes/{id}/shopping_cart/` POST-запрос – добавление нового рецепта в список покупок. DELETE-запрос – удаление рецепта из списка покупок. Доступно для авторизированных пользователей.

`/api/recipes/download_shopping_cart/` GET-запрос – получение текстового файла со списком покупок. Доступно для авторизированных пользователей.

`/api/users/{id}/subscribe/` GET-запрос – подписка на пользователя с указанным id. POST-запрос – отписка от пользователя с указанным id. Доступно для авторизированных пользователей

`/api/users/subscriptions/` GET-запрос – получение списка всех пользователей, на которых подписан текущий пользователь Доступно для авторизированных пользователей.