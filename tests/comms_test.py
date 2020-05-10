from requests import get, post, put, delete

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/comments', json={}).json())

# Некорректный запрос на добавление комментария: автор не числом
print(post('http://localhost:8080/api/comments', json=
           {
               'post_id': 1,
               'content': 'Круто!',
               'author': 'author'
           }).json()
      )

# Некорректный запрос на добавление комментария: пост не числом
print(post('http://localhost:8080/api/comments', json=
           {
               'post_id': 'one',
               'content': 'Еее!',
               'author': 5
           }).json()
      )

# Некорректный запрос на добавление комментария: нет обязательных данных
print(post('http://localhost:8080/api/comments', json=
           {
               'content': 'Отлично!',
           }).json()
      )

# Корректный запрос на добавление комментария
print(post('http://localhost:8080/api/comments', json=
           {
               'post_id': 3,
               'content': 'content',
               'author': 1
           }).json()
      )

# Вывод всех комментариев
print(get('http://localhost:8080/api/comments').json())

# Некорректный запрос: такого комментария нет
print(get('http://localhost:8080/api/comments/1000').json())

# Вывод информации об одном комментарии
print(get('http://localhost:8080/api/comments/1').json())

# Изменение информации о комментарие
print(put('http://localhost:8080/api/comments/2', json=
          {
              'content': 'Класс!'
          }
          ).json()
      )

# Удаление комментария
print(delete('http://localhost:8080/api/comments/2').json())
