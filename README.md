# Admiral-Markets - Python-Test-Assignment

Посмотреть и поработать с уже развернутым приложением можно по ссылке:
https://categories-api-lodka.herokuapp.com

Для развертывания на своей машине:
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver

Реализовано:
- POST /categories/ ('tree' - имя параметра POST запроса)
- GET /categories/2/ 
- GET /categories/delete/ (очистка всей БД)

![Иллюстрация к проекту](https://raw.githubusercontent.com/Egor14/lodka/master/tree.png)
