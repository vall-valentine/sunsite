from requests import get, post, delete

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/messages', json={}).json())

# Некорректный запрос на добавление сообщения: автор не числом
print(post('http://localhost:8080/api/messages', json=
           {
               'chat': 1,
               'content': 'content',
               'author': 'author'
           }
           ).json()
      )

# Некорректный запрос на добавление сообщения: автор не числом
print(post('http://localhost:8080/api/messages', json=
           {
               'chat': '1',
               'content': 'content',
               'author': 2
           }
           ).json()
      )

# Некорректный запрос на добавление поста: нет обязательных данных
print(post('http://localhost:8080/api/messages', json=
           {
               'chat': 'title',
               'content': 'content',
           }
           ).json()
      )

# Корректный запрос на добавление сообщения
print(post('http://localhost:8080/api/messages', json=
           {
                'chat': 1,
                'content': 'content',
                'author': 1
           }
           ).json()
      )

# Вывод всех сообщений
print(get('http://localhost:8080/api/messages').json())

# Некорректный запрос: такого сообщения нет
print(get('http://localhost:8080/api/messages/1000').json())

# Вывод информации об одном сообщении
print(get('http://localhost:8080/api/messages/1').json())

# Удаление сообщении
print(delete('http://localhost:8080/api/messages/2').json())
