from requests import get, post, put, delete

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/posts', json={}).json())

# Некорректный запрос на добавление поста: автор не числом
print(post('http://localhost:8080/api/posts', json=
           {
               'title': 'title',
               'content': 'content',
               'author': 'author'
           }
           ).json()
      )

# Некорректный запрос на добавление поста: нет обязательных данных
print(post('http://localhost:8080/api/posts', json=
           {
               'title': 'title',
               'content': 'content',
           }
           ).json()
      )

# Корректный запрос на добавление поста
print(post('http://localhost:8080/api/posts', json=
            {
                'title': 'title',
                'content': 'content',
                'author': 1
            }
           ).json()
      )

# Вывод всех постов
print(get('http://localhost:8080/api/posts').json())

# Некорректный запрос: такого поста нет
print(get('http://localhost:8080/api/posts/1000').json())

# Вывод информации об одном посте
print(get('http://localhost:8080/api/posts/1').json())

# Изменение информации о посте
print(put('http://localhost:8080/api/posts/2', json=
          {
              'title': 'another title'
          }).json()
      )

# Удаление поста
print(delete('http://localhost:8080/api/posts/2').json())

# Вывод информации о чатах пользователя
print(delete('http://localhost:8080/api/posts/2').json())
