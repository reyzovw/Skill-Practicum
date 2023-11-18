import psycopg2
from .sql import PostgreQuery
from hashlib import sha256
from time import time
from random import choice
from datetime import datetime
from base64 import b64encode


# ----------------- Microservices ---------------

class Encrypt:
    def to_hash(self, text: str):
        text_bytes = text.encode('utf-8')
        sha256_hash = sha256()
        sha256_hash.update(text_bytes)
        hashed_text = sha256_hash.hexdigest()

        return hashed_text


# -------------------- Users --------------------

db_params = {
            'host': 'localhost',
            'database': 'factorial',
            'user': 'admin',
            'password': 'factorial',
            'port': '5432'
        }

class UsersDatabase:
    def __init__(self):
        self.__connection = psycopg2.connect(**db_params)
        query = """
        CREATE TABLE IF NOT EXISTS users_db (
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar BYTEA
        );
        """
        with PostgreQuery(self.__connection, query): ...

    def register_user(self, username: str, email: str, password: str):
        try:
            password_hash = Encrypt().to_hash(str(password))
            avatar = open("static/images/avatar.png", 'rb')
            # avatar_bytes = b64encode(avatar.read()).decode("utf-8")
            avatar_bytes = avatar.read()
            avatar.close()
            query = """
            INSERT INTO users_db (
                username,
                email,
                password_hash,
                avatar
            )
            VALUES (%s, %s, %s, %s)
            """
            with PostgreQuery(self.__connection, (query, (username, email, password_hash, avatar_bytes))):
                return "Пользователь успешно зарегистрирован"
        except Exception as e:
            print(e)
            return "Пользователь уже зарегистрирован"

    def get_user_by_id(self, user_id: int):
        with PostgreQuery(self.__connection, ("SELECT * FROM users_db WHERE user_id = %s", (user_id,))) as result:
            try:
                arr = []
                for element in result[0]:
                    arr.append(element)
                arr[4] = bytes(arr[4])
                arr[4] = b64encode(arr[4]).decode('utf-8')
                return arr
            except IndexError:
                return "Пользователь не найден"

    def get_user_by_username(self, username: str):
        with PostgreQuery(self.__connection, ("SELECT * FROM users_db WHERE username = %s", (username,))) as result:
            try:
                arr = []
                for element in result[0]:
                    arr.append(element)
                arr[4] = bytes(arr[4])
                arr[4] = b64encode(arr[4]).decode('utf-8')
                return arr
            except IndexError:
                return "Пользователь не найден"

    def login_user(self, username: str, password: str):
        result = self.get_user_by_username(username)
        if result != "Пользователь не найден" and result[3] == Encrypt().to_hash(password):
            return True  # Вход выполнен успешно

        return False  # Не удалось войти


# ------------------- Skills --------------------

class SkillsDatabase:
    def __init__(self):
        self.__connection = psycopg2.connect(**db_params)
        query = """
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            skill_title TEXT NOT NULL,
            skill_description TEXT
        );
        """
        with PostgreQuery(self.__connection, query): ...

    def set_skill_to_user(self, user_id: int, skill_title: str, skill_description=""):
        query = """
        INSERT INTO skills (user_id, skill_title, skill_description) VALUES (%s, %s, %s)
        """
        with PostgreQuery(self.__connection, (query, (user_id, skill_title, skill_description))): ...

    def get_user_skills_by_id(self, user_id: int):
        query = """
        SELECT * FROM skills WHERE user_id = %s 
        """
        with PostgreQuery(self.__connection, (query, (user_id,))) as result:
            try:
                return result
            except IndexError:
                return "Пользователь еще не выбрал навыков"

# ------------------- Feed --------------------

class FeedManager:
    def __init__(self):
        self.__connection = psycopg2.connect(**db_params)
        query = """
                CREATE TABLE IF NOT EXISTS feed (
                    post_id SERIAL PRIMARY KEY,
                    from_user_id INTEGER NOT NULL,
                    post_text TEXT NOT NULL,
                    datetime INTEGER NOT NULL,
                    likes INTEGER,
                    likes_by TEXT
                );
                """
        # добавить лайки и кто лайкал
        with PostgreQuery(self.__connection, query): ...

    def create_post(self, from_user_id: int, text: str):
        default_likes_by = []
        unix_time = int(str(time()).split(".")[0])
        date = datetime.utcfromtimestamp(unix_time).strftime('%d-%m в %H:%M')
        query = """
        INSERT INTO feed (from_user_id, post_text, datetime, likes, likes_by) VALUES (%s, %s, %s, 0, %s)
        """
        try:
            with PostgreQuery(self.__connection, (query, (from_user_id, text, date, str(default_likes_by)))): ...
            return "Пост был выложен"
        except Exception as e:
            return f"При выкладывании поста произошла ошибка: {e}"

    def get_post_by_id(self, post_id: int):
        with PostgreQuery(self.__connection, ("SELECT * FROM feed WHERE post_id = %s", (post_id, ))) as result:
            return result

    def get_random_posts(self):
        posts = set()
        with PostgreQuery(self.__connection, "SELECT * FROM feed LIMIT 10") as result:
            try:
                for _ in range(len(result)):
                    posts.add(choice(result))
            except IndexError:
                return ["Постов нету"] # в массиве что бы не было ошибки

        return posts
