# Skill Practicum

## Стек

![Python](https://img.shields.io/badge/python-3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%238A4182.svg?style=for-the-badge&logo=flask&logoColor=white) ![Gmail](https://img.shields.io/badge/Mail.ru-%231877F2?style=for-the-badge&logo=gmail&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Информация

Factorial - это социальная сеть, основанная на мгновенном обмене знаний и навыков с использованием кратких видео-роликов и постов.

Цель платформы - объединить людей через обмен интересными и полезными навыками, уникальными знаниями и творческими идеями.

Мгновенный обмен: Платформа поощряет быстрый и легкий обмен знаний. Пользователи могут подписываться на других, ставить лайки, обсуждать и делиться контентом с минимальными усилиями.

Группы по интересам: Пользователи могут объединяться в группы по интересам, где обсуждают свои хобби, делятся советами и организовывают совместные проекты.

*Factorial* [release manager](https://wonderful-zydeco-56f.notion.site/de467a31a964479ca07027f515a05808?v=b260327d37e54a85aa64ea47f6fd5033)

## Запуск

Шаг 1: Если мы не скачали *Docker-Desktop* то скачиваем, так же скачиваем *WSL*

Шаг 2: Создаем пустую папку и инитиализируем *git*
```commandline
git init
```
Шаг 3: Клонируем репозиторий в нашу локальную папку
```commandline
git clone https://github.com/reyzovw/Skill-Practicum
```
Шаг 4: Переходим в папку которая появлась после *git clone*
```commandline
cd Skill-Practicum
```
Шаг 5: Создаем и настраиваем наш *Docker* контейнер
```commandline
docker-compose build
```
Шаг 6: Запускаем наш *Docker* контейнер
```commandline
docker-compose up -d
```

*Если понадобилось остановить контейнер*
```commandline
docker-compose stop
```
*Если понадобилось удалить контейнер*
```commandline
docker-compose down
```
*Если понадобилось запустить контейнер и добавить в него новые изменения*
```commandline
docker-compose up -d --build
```