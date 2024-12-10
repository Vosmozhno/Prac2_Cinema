import datetime
from tabulate import tabulate 
from functools import reduce

# Данные
users = [
    {"username": "admin", "password": "admin", "role": "admin"},
    {"username": "user1", "password": "1234", "role": "user", "subscription_type": "Basic", "history": [], "created_at": "2024-09-01"}
]

movies = [
    {"title": "Интерстеллар", "genre": "Sci-Fi", "rating": 8.6, "release_date": "2014-11-07"},
    {"title": "Начало", "genre": "Thriller", "rating": 8.8, "release_date": "2010-07-16"}
]

# Функции для пользователей

def authenticate():
    print("Добро пожаловать в онлайн-кинотеатр!")
    username = input("Логин: ").strip()
    if username.lower() == "exit":
        print("Выход из программы.")
        exit()  # Завершаем программу, если введен "exit"

    password = input("Пароль: ").strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return user

    print("Неверный логин или пароль.")
    return None

def view_movies():
    print("\nСписок фильмов:")
    if not movies:
        print("Нет доступных фильмов.")
        return
    table = [[movie["title"], movie["genre"], movie["rating"], movie["release_date"]] for movie in movies]
    print(tabulate(table, headers=["Название", "Жанр", "Рейтинг", "Дата выхода"], tablefmt="grid"))

def sort_movies():
    try:
        criterion = input("\nСортировать по (rating/release_date): ").strip().lower()
        if criterion not in ["rating", "release_date"]:
            raise ValueError("Некорректный критерий.")
        sorted_movies = sorted(movies, key=lambda x: x[criterion], reverse=True)
        table = [[movie["title"], movie["genre"], movie["rating"], movie["release_date"]] for movie in sorted_movies]
        print(tabulate(table, headers=["Название", "Жанр", "Рейтинг", "Дата выхода"], tablefmt="grid"))
    except ValueError as e:
        print(e)

def filter_movies():
    try:
        keyword = input("\nВведите ключевое слово для поиска по названию: ").strip().lower()
        filtered = list(filter(lambda x: keyword in x["title"].lower(), movies))
        if filtered:
            table = [[movie["title"], movie["genre"], movie["rating"], movie["release_date"]] for movie in filtered]
            print(tabulate(table, headers=["Название", "Жанр", "Рейтинг", "Дата выхода"], tablefmt="grid"))
        else:
            print("Фильмы не найдены.")
    except Exception as e:
        print(f"Ошибка: {e}")

def buy_subscription(user):
    print("\nДоступные подписки: Basic, Premium")
    subscription = input("Выберите подписку: ").strip()
    if subscription in ["Basic", "Premium"]:
        user["subscription_type"] = subscription
        print(f"Подписка {subscription} успешно оформлена!")
    else:
        print("Некорректная подписка.")

def view_history(user):
    print("\nИстория просмотров:")
    if not user.get("history"):
        print("История пуста.")
    else:
        print("\n".join(user["history"]))

def update_password(user):
    """Изменение пароля пользователя."""
    current_password = input("Введите текущий пароль: ").strip()
    if current_password == user["password"]:
        new_password = input("Введите новый пароль: ").strip()
        confirm_password = input("Подтвердите новый пароль: ").strip()
        if new_password == confirm_password:
            user["password"] = new_password
            print("Пароль успешно обновлён!")
        else:
            print("Пароли не совпадают.")
    else:
        print("Неверный текущий пароль.")

def view_account(user):
    """Просмотр информации о аккаунте пользователя."""
    print("\nИнформация о вашем аккаунте:")
    print(f"Логин: {user['username']}")
    print(f"Роль: {user['role']}")
    print(f"Тип подписки: {user.get('subscription_type', 'Нет')}")
    print(f"Дата создания аккаунта: {user['created_at']}")
    print(f"История просмотров: {', '.join(user.get('history', [])) if user.get('history') else 'Нет истории'}")

def watch_movie(user):
    """Функция для просмотра фильма и добавления его в историю по названию."""
    print("\nВведите название фильма для просмотра:")
    movie_title = input().strip()

    movie = next((movie for movie in movies if movie['title'].lower() == movie_title.lower()), None)

    if movie:
        # Если фильм найден, добавляем его в историю
        if movie['title'] not in user['history']:
            user['history'].append(movie['title'])
            print(f"Вы успешно просмотрели фильм: {movie['title']}")
        else:
            print(f"Вы уже просмотрели фильм: {movie['title']}")
    else:
        print(f"Фильм с названием '{movie_title}' не найден.")


# Функции для администратора

def add_movie():
    """Добавление нового фильма."""
    try:
        title = input("Название фильма: ").strip()
        genre = input("Жанр: ").strip()
        rating = float(input("Рейтинг: ").strip())
        release_date = input("Дата выхода (YYYY-MM-DD): ").strip()
        movies.append({"title": title, "genre": genre, "rating": rating, "release_date": release_date})
        print("Фильм добавлен.")
    except ValueError:
        print("Ошибка ввода. Проверьте данные.")

def delete_movie():
    """Удаление фильма."""
    view_movies()
    try:
        idx = int(input("Введите номер фильма для удаления: ")) - 1
        if idx < 0 or idx >= len(movies):
            raise IndexError
        deleted = movies.pop(idx)
        print(f"Фильм '{deleted['title']}' удален.")
    except (ValueError, IndexError):
        print("Некорректный ввод.")

def edit_movie():
    """Редактирование данных о фильме."""
    view_movies()
    try:
        idx = int(input("Введите номер фильма для редактирования: ")) - 1
        if idx < 0 or idx >= len(movies):
            raise IndexError
        movie = movies[idx]
        print(f"Редактирование фильма: {movie['title']}")
        title = input(f"Новое название (оставьте пустым для сохранения '{movie['title']}'): ").strip()
        genre = input(f"Новый жанр (оставьте пустым для сохранения '{movie['genre']}'): ").strip()
        rating = input(f"Новый рейтинг (оставьте пустым для сохранения '{movie['rating']}'): ").strip()
        release_date = input(f"Новая дата выхода (оставьте пустым для сохранения '{movie['release_date']}'): ").strip()

        if title: movie["title"] = title
        if genre: movie["genre"] = genre
        if rating: movie["rating"] = float(rating)
        if release_date: movie["release_date"] = release_date
        
        print(f"Фильм '{movie['title']}' успешно отредактирован.")
    except (ValueError, IndexError):
        print("Некорректный ввод.")

def manage_users():
    """Управление пользователями."""
    print("\nПользователи:")
    for idx, user in enumerate(users):
        print(f"{idx + 1}. {user['username']} | Роль: {user['role']} | Подписка: {user.get('subscription_type', 'Нет')}")
    
    action = input("Добавить/Удалить/Изменить пользователя (add/delete/edit): ").strip().lower()
    
    if action == "add":
        username = input("Логин: ").strip()
        password = input("Пароль: ").strip()
        role = input("Роль (admin/user): ").strip()
        users.append({"username": username, "password": password, "role": role})
        print("Пользователь добавлен.")
    
    elif action == "delete":
        idx = int(input("Введите номер пользователя для удаления: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Некорректный номер.")
            return
        deleted = users.pop(idx)
        print(f"Пользователь '{deleted['username']}' удален.")
    
    elif action == "edit":
        idx = int(input("Введите номер пользователя для редактирования: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Некорректный номер.")
            return
        user = users[idx]
        print(f"Редактирование пользователя: {user['username']}")
        new_username = input(f"Новый логин (оставьте пустым для сохранения '{user['username']}'): ").strip()
        new_password = input(f"Новый пароль (оставьте пустым для сохранения): ").strip()
        new_role = input(f"Новая роль (оставьте пустым для сохранения '{user['role']}'): ").strip()
        
        if new_username: user["username"] = new_username
        if new_password: user["password"] = new_password
        if new_role: user["role"] = new_role
        
        print(f"Пользователь '{user['username']}' успешно отредактирован.")
    else:
        print("Некорректное действие.")

def view_statistics():
    """Просмотр статистики."""
    print("\nСтатистика:")
    print(f"Общее количество фильмов: {len(movies)}")
    print(f"Общее количество пользователей: {len(users)}")
    
    movie_views = {}
    for user in users:
        for movie in user.get("history", []):
            if movie in movie_views:
                movie_views[movie] += 1
            else:
                movie_views[movie] = 1

    sorted_movies = sorted(movie_views.items(), key=lambda x: x[1], reverse=True)
    print("\nТоп популярных фильмов:")
    for movie, views in sorted_movies[:5]:  # Показываем только топ 5
        print(f"{movie}: {views} просмотров")

def view_user_history():
    """Просмотр истории пользователей."""
    print("\nИстория пользователей:")
    for idx, user in enumerate(users):
        print(f"{idx + 1}. {user['username']} - История просмотров:")
        if user.get("history"):
            for movie in user["history"]:
                print(f"  - {movie}")
        else:
            print("  Нет истории.")

# Функции с использованием map, filter, reduce, zip

def capitalize_movie_titles():
    """Используем map для преобразования названий фильмов в формат с заглавной буквы."""
    global movies
    movies = list(map(lambda movie: {**movie, 'title': movie['title'].capitalize()}, movies))
    print("Названия фильмов изменены.")

def filter_movies_by_rating(rating_threshold):
    """Используем filter для фильтрации фильмов с рейтингом выше заданного значения."""
    filtered_movies = list(filter(lambda movie: movie['rating'] > rating_threshold, movies))
    if filtered_movies:
        table = [[movie["title"], movie["genre"], movie["rating"], movie["release_date"]] for movie in filtered_movies]
        print(tabulate(table, headers=["Название", "Жанр", "Рейтинг", "Дата выхода"], tablefmt="grid"))
    else:
        print(f"Фильмы с рейтингом выше {rating_threshold} не найдены.")

def total_movie_rating():
    """Используем reduce для подсчёта общего рейтинга всех фильмов."""
    total_rating = reduce(lambda acc, movie: acc + movie['rating'], movies, 0)
    print(f"Общий рейтинг всех фильмов: {total_rating}")

def zip_movie_titles_with_indices():
    """Используем zip для объединения индексов фильмов с их названиями."""
    movie_indices = list(zip(range(1, len(movies) + 1), [movie['title'] for movie in movies]))
    for idx, title in movie_indices:
        print(f"Фильм {idx}: {title}")

# Основной цикл
def main():
    while True:
        user = authenticate()
        if user:
            if user["role"] == "admin":
                while True:
                    print("\n1. Добавить фильм")
                    print("2. Удалить фильм")
                    print("3. Редактировать фильм")
                    print("4. Просмотреть фильмы")
                    print("5. Просмотреть статистику")
                    print("6. Просмотр действий пользователей")
                    print("7. Выйти")
                    
                    choice = input("Выберите действие: ").strip()
                    if choice == "1":
                        add_movie()
                    elif choice == "2":
                        delete_movie()
                    elif choice == "3":
                        edit_movie()
                    elif choice == "4":
                        view_movies()
                    elif choice == "5":
                        total_movie_rating()  # Пример использования reduce
                        filter_movies_by_rating(7.5)  # Пример использования filter
                        capitalize_movie_titles()  # Пример использования map
                        zip_movie_titles_with_indices()  # Пример использования zip
                    elif choice == "6":
                        view_user_history()
                    elif choice == "7":
                        print("Выход из программы.")
                        return  # Завершаем программу
                    else:
                        print("Некорректный выбор.")
            elif user["role"] == "user":
                while True:
                    print("\n1. Просмотреть фильмы")
                    print("2. Сортировать фильмы")
                    print("3. Фильтровать фильмы")
                    print("4. Купить подписку")
                    print("5. Просмотреть аккаунт")  # Добавлен пункт для просмотра аккаунта
                    print("6. Просмотреть фильм")  # Добавлен пункт для просмотра фильма
                    print("7. Выйти")
                    
                    choice = input("Выберите действие: ").strip()
                    if choice == "1":
                        view_movies()
                    elif choice == "2":
                        sort_movies()
                    elif choice == "3":
                        filter_movies()
                    elif choice == "4":
                        buy_subscription(user)
                    elif choice == "5":
                        view_account(user)  # Вызов функции для просмотра аккаунта
                    elif choice == "6":
                        watch_movie(user)  # Вызов функции для просмотра фильма
                    elif choice == "7":
                        print("Выход из программы.")
                        return  # Завершаем программу
                    else:
                        print("Некорректный выбор.")

if __name__ == "__main__":
    main()