from requests import get, post, put, delete

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/users', json={}).json())

# Корректный запрос на добавление пользователя
print(post('http://localhost:8080/api/users', json=
           {
               'nickname': 'qwerty21',
               'surname': 'surname',
               'name': 'name',
               'about': 'about',
               'email': 'emai1l12@qw.qww',
               'age': 1,
               'password': 'password',
               'achievements': '1, 2'
           }
           ).json())

# Вывод всех пользователей
print(get('http://localhost:8080/api/users').json())

# Некорректный запрос: такого пользователя нет
print(get('http://localhost:8080/api/users/1000').json())

# Вывод информации об одном пользователе
print(get('http://localhost:8080/api/users/1').json())

# Изменение информации о пользователе
print(put('http://localhost:8080/api/users/4', json=
          {
            'surname': 'Se',
            'name': 'Nme',
            'about': 'About',
            'email': 'emfdsd@mail.ru'
          }
          ).json()
      )

# Удаление ползователя
print(delete('http://localhost:8080/api/users/3').json())
