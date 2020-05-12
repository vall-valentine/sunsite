from requests import get, post, put, delete

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/users', json={}).json())

# Некорректный запрос на добавление пользователя: возраст не числом
print(post('http://localhost:8080/api/users', json=
           {
               'nickname': 'qwerty21',
               'surname': 'surname',
               'name': 'name',
               'about': 'about',
               'email': 'emai1l12@qw.qww',
               'age': 'one',
               'password': 'password'
           }
           ).json()
      )

# Некорректный запрос на добавление пользователя: нет обязательных данных
print(post('http://localhost:8080/api/users', json=
           {
               'nickname': 'qwerty21',
               'surname': 'surname',
               'name': 'name',
               'about': 'about',
               'age': 1,
               'password': 'password'
           }
           ).json()
      )

# Корректный запрос на добавление пользователя
print(post('http://localhost:8080/api/users', json=
           {
               'nickname': 'qwerty21',
               'surname': 'surname',
               'name': 'name',
               'about': 'about',
               'email': 'email@email.ru',
               'age': 1,
               'password': 'password'
           }
           ).json()
      )

# Вывод всех пользователей
print(get('http://localhost:8080/api/users').json())

# Некорректный запрос: такого пользователя нет
print(get('http://localhost:8080/api/users/1000').json())

# Вывод информации об одном пользователе
print(get('http://localhost:8080/api/users/1').json())

# Некорректное изменение информации о пользователе
print(put('http://localhost:8080/api/users/4', json=
          {
              'nickname': 'qwerty',
              'surname': 'Se',
              'name': 'Nme',
              'about': 'About',
              'email': 'qwerty@qwerty.qwerty'
          }
          ).json()
      )

# Изменение информации о пользователе
print(put('http://localhost:8080/api/users/4', json=
          {
              'nickname': 'qwerty1',
              'surname': 'Se',
              'name': 'Nme',
              'about': 'About',
              'email': 'qwerty1@qwerty.qwerty'
          }
          ).json()
      )

# Удаление ползователя
print(delete('http://localhost:8080/api/users/3').json())

# Вывод информации о чатах пользователя
print(get('http://localhost:8080/api/users/1/chats'))