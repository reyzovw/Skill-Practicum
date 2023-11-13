from sqlite3 import connect, IntegrityError
from .sql import Query
from hashlib import sha256
from time import time
from random import choice
from datetime import datetime


# ----------------- Microservices ---------------

class Encrypt:
    def to_hash(self, text: str):
        text_bytes = text.encode('utf-8')
        sha256_hash = sha256()
        sha256_hash.update(text_bytes)
        hashed_text = sha256_hash.hexdigest()

        return hashed_text


# -------------------- Users --------------------

class UsersDatabase:
    def __init__(self):
        self.__connection = connect("test_users.db", check_same_thread=False, cached_statements=True)
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
        with Query(self.__connection, query): ...

    def register_user(self, username: str, email: str, password: str):
        try:
            password_hash = Encrypt().to_hash(str(password))
            query = """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """
            with Query(self.__connection, (query, (username, email, password_hash))):
                return "Пользователь успешно зарегистрирован"
        except IntegrityError as e:
            return "Пользователь уже зарегистрирован"

    def get_user_by_id(self, user_id: int):
        with Query(self.__connection, ("SELECT * FROM users WHERE user_id = ?", (user_id,))) as result:
            try:
                return result[0]
            except IndexError:
                return "Пользователь не найден"

    def get_user_by_username(self, username: str):
        with Query(self.__connection, ("SELECT * FROM users WHERE username = ?", (username,))) as result:
            try:
                return result[0]
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
        self.__connection = connect("test_skills.db", check_same_thread=False, cached_statements=True)
        query = """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_title TEXT NOT NULL,
            skill_description TEXT
        )
        """
        with Query(self.__connection, query): ...

    def set_skill_to_user(self, user_id: int, skill_title: str, skill_description=""):
        query = """
        INSERT INTO skills (user_id, skill_title, skill_description) VALUES (?, ?, ?)
        """
        with Query(self.__connection, (query, (user_id, skill_title, skill_description))): ...

    def get_user_skills_by_id(self, user_id: int):
        query = """
        SELECT skill_title, skill_description FROM skills WHERE user_id = ? 
        """
        with Query(self.__connection, (query, (user_id,))) as result:
            try:
                return result
            except IndexError:
                return "Пользователь еще не выбрал навыков"

    # stopship 13.11 0:20
    # Доделать завтра, сделать что бы были навыки как на хабр карьера, по типу гита и того подобного
    # https://chat.openai.com/c/463b17ed-8e7c-48dc-97d6-7beb9267974d


# ------------------- Feed --------------------

class FeedManager:
    def __init__(self):
        self.__connection = connect("test_feed.db", check_same_thread=False, cached_statements=True)
        query = """
                CREATE TABLE IF NOT EXISTS feed (
                    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_user_id INTEGER NOT NULL,
                    post_text TEXT NOT NULL,
                    datetime INTEGER NOT NULL
                )
                """
        with Query(self.__connection, query): ...

    def create_post(self, from_user_id: int, text: str):
        unix_time = int(str(time()).split(".")[0])
        date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M')
        query = """
        INSERT INTO feed (from_user_id, post_text, datetime) VALUES (?, ?, ?)
        """
        try:
            with Query(self.__connection, (query, (from_user_id, text, date))): ...
            return "Пост был выложен"
        except Exception as e:
            return f"При выкладывании поста произошла ошибка: {e}"

    def get_post_by_id(self, post_id: int):
        with Query(self.__connection, ("SELECT * FROM feed WHERE post_id = ?", (post_id, ))) as result:
            return result

    def get_random_posts(self):
        posts = set()
        with Query(self.__connection, "SELECT * FROM feed LIMIT 50") as result:
            try:
                for _ in range(10):
                    posts.add(choice(result))
            except IndexError:
                return ["Постов нету"] # в массиве что бы не было ошибки

        return posts
