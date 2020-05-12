from requests import get, post, delete, put

# Некорректный запрос: пустой запрос
print(post('http://localhost:8080/api/chats', json={}).json())

# Корректный запрос на добавление чата
print(post('http://localhost:8080/api/chats', json=
           {
               'users': '1 2',
               'title': 'Первый чат!'
           }).json()
      )

# Корректный запрос на изменения чата
print(put('http://localhost:8080/api/chats/1', json=
          {
               'users': '1 2 3',
               'title': 'Шучу, не первый!'
          }).json()
      )

# Вывод всех чатов
print(get('http://localhost:8080/api/chats').json())

# Некорректный запрос: такого чата нет
print(get('http://localhost:8080/api/chats/1000').json())

# Вывод информации об одном чате
print(get('http://localhost:8080/api/chats/1').json())

# Удаление чата
print(delete('http://localhost:8080/api/chats/2').json())
